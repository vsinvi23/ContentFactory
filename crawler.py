#!/usr/bin/env python3
"""
Playwright-based Course & Web Content Crawler with Persistent Chrome Session (Method 3).
"""

import argparse
import asyncio
import os
import re
import sys
import time
import urllib.parse
from pathlib import Path
from playwright.async_api import async_playwright, BrowserContext, Page

from extractor import clean_html


def extract_course_name(url: str, page_title: str = "") -> str:
    """
    Extracts a sanitized course name from the URL or page title.
    """
    parsed = urllib.parse.urlparse(url)
    parts = [p for p in parsed.path.split('/') if p]

    for idx, part in enumerate(parts):
        if part in ["courses", "course", "collection", "learn", "module", "paths"] and idx + 1 < len(parts):
            course_slug = parts[idx + 1]
            # Replace dashes with underscores and clean characters
            clean_slug = re.sub(r'[\\/*?:"<>|]', "", course_slug).strip()
            if clean_slug:
                return clean_slug

    # Fallback to page title or domain
    if page_title:
        clean = re.sub(r'[\\/*?:"<>|]', "", page_title).strip()
        # Take first part of title before any separator like |, -, —
        first_segment = re.split(r"[-|—•]", clean)[0].strip()
        if first_segment:
            return re.sub(r"\s+", "_", first_segment)[:50]

    return "course_content"


async def extract_course_structure(page: Page, course_base: str):
    """
    Extracts all chapters and lessons from the course navigation sidebar.
    """
    return await page.evaluate(
        """(courseBase) => {
            const nav = document.querySelector("nav") || document.querySelector("aside") || document.querySelector("#drawer") || document.body;
            if (!nav) return [];

            const allElements = Array.from(nav.querySelectorAll("h5, a[href*='" + courseBase + "/']"));
            
            const chaptersMap = [];
            let currentChapter = "1. Introduction";
            let currentLessons = [];

            for (const el of allElements) {
                if (el.tagName === "H5" && /^\\d+\\./.test(el.innerText.trim())) {
                    if (currentLessons.length > 0) {
                        chaptersMap.push({ chapter: currentChapter, lessons: currentLessons });
                        currentLessons = [];
                    }
                    currentChapter = el.innerText.trim().replace(/\\n+/g, " ");
                } else if (el.tagName === "A") {
                    let href = el.getAttribute("href");
                    if (!href || href === courseBase || href === courseBase + "/" || href.includes("#")) continue;
                    if (!href.startsWith("http")) href = "https://www.educative.io" + href;
                    
                    const title = el.innerText.trim().split("\\n")[0];
                    if (!currentLessons.some(l => l.url === href)) {
                        currentLessons.push({ title: title, url: href });
                    }
                }
            }
            if (currentLessons.length > 0) {
                chaptersMap.push({ chapter: currentChapter, lessons: currentLessons });
            }
            return chaptersMap;
        }""",
        course_base
    )


async def crawl_course_hierarchy(
    page: Page,
    course_name: str,
    base_output_dir: Path,
    args
):
    """
    Crawl every chapter and section/lesson in the course hierarchy,
    organize files into chapter subfolders, and write an INDEX.md summary.
    """
    course_base = f"/courses/{course_name}"
    print(f"\n[+] Extracting course structure for: {course_base}...")

    # If currently on the course marketing/overview page, find the first lesson link
    # to open the reader interface where the navigation drawer is fully loaded.
    curr_clean_url = page.url.rstrip("/")
    if curr_clean_url.endswith(course_name):
        first_lesson = await page.evaluate(
            """(courseBase) => {
                const links = Array.from(document.querySelectorAll("a[href*='" + courseBase + "/']"));
                for (const a of links) {
                    const href = a.getAttribute("href");
                    if (href && href !== courseBase && href !== courseBase + "/" && !href.includes("#")) {
                        return href.startsWith("http") ? href : "https://www.educative.io" + href;
                    }
                }
                return null;
            }""",
            course_base
        )
        if first_lesson:
            print(f"[+] Opening first lesson to load course reader drawer: {first_lesson}...")
            try:
                await page.goto(first_lesson, wait_until="networkidle", timeout=45000)
            except Exception:
                await page.goto(first_lesson, wait_until="load", timeout=30000)
            await asyncio.sleep(2)
    
    chapters = await extract_course_structure(page, course_base)

    # Fallback if no H5 structure found: gather all unique course lesson links
    if not chapters:
        print("[!] No H5 chapter headers detected. Falling back to page link extraction...")
        fallback_links = await page.evaluate(
            """(courseBase) => {
                const links = Array.from(document.querySelectorAll("a[href*='" + courseBase + "/']"));
                const items = [];
                const seen = new Set();
                for (const a of links) {
                    let href = a.getAttribute("href");
                    if (!href || href === courseBase || href === courseBase + "/" || href.includes("#")) continue;
                    if (!href.startsWith("http")) href = "https://www.educative.io" + href;
                    if (!seen.has(href)) {
                        seen.add(href);
                        items.push({
                            title: a.innerText.trim().split("\\n")[0] || href.split("/").pop(),
                            url: href
                        });
                    }
                }
                return items;
            }""",
            course_base
        )
        if fallback_links:
            chapters = [{"chapter": "1. Course Content", "lessons": fallback_links}]

    if not chapters:
        print(f"[!] Could not find any course lessons for: {course_name}")
        return

    total_chapters = len(chapters)
    total_lessons = sum(len(c.get("lessons", [])) for c in chapters)

    course_dir = base_output_dir / course_name
    course_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 65)
    print(f" COURSE DISCOVERED: {course_name}")
    print(f" Total Chapters: {total_chapters}")
    print(f" Total Sections / Lessons: {total_lessons}")
    print(f" Target Directory: {course_dir.resolve()}")
    print("=" * 65 + "\n")

    summary_records = []
    downloaded_count = 0
    skipped_count = 0
    index_md_content = [
        f"# {course_name.replace('-', ' ').title()}\n",
        f"**Total Chapters:** {total_chapters} | **Total Lessons:** {total_lessons}\n",
        "## Table of Contents\n"
    ]

    for ch_idx, ch_info in enumerate(chapters, start=1):
        raw_ch_name = ch_info.get("chapter", f"Chapter {ch_idx}")
        # Clean chapter name for directory
        clean_ch_name = re.sub(r'[\\/*?:"<>|]', "", raw_ch_name).strip()
        clean_ch_name = re.sub(r"\s+", "_", clean_ch_name)
        ch_dir_name = f"{ch_idx:02d}_{clean_ch_name}"
        ch_output_dir = course_dir / ch_dir_name
        ch_output_dir.mkdir(parents=True, exist_ok=True)

        lessons = ch_info.get("lessons", [])
        print(f"\n[{ch_idx}/{total_chapters}] Chapter: {raw_ch_name} ({len(lessons)} lessons)")
        index_md_content.append(f"\n### {raw_ch_name}\n")

        ch_downloaded = 0
        ch_skipped = 0

        for les_idx, les_info in enumerate(lessons, start=1):
            les_title = les_info.get("title", f"Lesson {les_idx}")
            les_url = les_info.get("url")

            clean_les_title = re.sub(r'[\\/*?:"<>|]', "", les_title).strip()
            clean_les_title = re.sub(r"\s+", "_", clean_les_title)[:70]
            target_file = ch_output_dir / f"{les_idx:02d}_{clean_les_title}.md"

            rel_link = f"{ch_dir_name}/{les_idx:02d}_{clean_les_title}.md"
            index_md_content.append(f"- [{les_title}]({rel_link})")

            # Check if already downloaded
            if target_file.exists() and target_file.stat().st_size > 500 and not args.force:
                print(f"    [{les_idx}/{len(lessons)}] (Skipped, already exists) {target_file.name}")
                skipped_count += 1
                ch_skipped += 1
                continue

            # If this is the active page already loaded, don't navigate on first page
            should_navigate = (page.url != les_url)
            await crawl_page(
                page=page,
                url=les_url,
                output_dir=ch_output_dir,
                selector=args.selector,
                scroll=args.scroll,
                save_format=args.format,
                index=les_idx,
                navigate=should_navigate
            )
            downloaded_count += 1
            ch_downloaded += 1

            if les_idx < len(lessons):
                await asyncio.sleep(args.delay)

        summary_records.append({
            "chapter": raw_ch_name,
            "total": len(lessons),
            "downloaded": ch_downloaded,
            "skipped": ch_skipped
        })

    # Write INDEX.md
    index_file = course_dir / "INDEX.md"
    with open(index_file, "w", encoding="utf-8") as f:
        f.write("\n".join(index_md_content))
    print(f"\n[+] Course Index created: {index_file.resolve()}")

    # Localize all images for full offline viewing
    try:
        from localize_images import localize_all_course_images
        localize_all_course_images(course_dir)
    except Exception as e:
        print(f"[!] Warning: Image localization encountered an issue: {e}")

    # Print Final Summary
    print("\n" + "=" * 65)
    print(" DOWNLOAD SUMMARY:")
    print("=" * 65)
    for rec in summary_records:
        status_str = f"{rec['downloaded']} downloaded"
        if rec['skipped']:
            status_str += f", {rec['skipped']} already existed"
        print(f"  • {rec['chapter']}: {status_str} (out of {rec['total']})")
    print("-" * 65)
    print(f" Total Chapters Processed: {total_chapters}")
    print(f" Total Sections Downloaded: {downloaded_count}")
    if skipped_count:
        print(f" Total Sections Skipped (cached): {skipped_count}")
    print(f" All files organized inside: {course_dir.resolve()}")
    print("=" * 65 + "\n")


async def auto_scroll(page: Page, scroll_delay: float = 0.5):
    """
    Gradually scrolls down the page to trigger lazy loading of images,
    interactive code widgets, and deferred DOM elements.
    """
    try:
        last_height = await page.evaluate("() => document.body.scrollHeight")
        while True:
            await page.evaluate("() => window.scrollBy(0, window.innerHeight)")
            await asyncio.sleep(scroll_delay)
            new_height = await page.evaluate("() => document.body.scrollHeight")
            current_scroll = await page.evaluate("() => window.pageYOffset + window.innerHeight")
            if current_scroll >= new_height or new_height == last_height:
                break
            last_height = new_height
        # Scroll back to top
        await page.evaluate("() => window.scrollTo(0, 0)")
        await asyncio.sleep(0.5)
    except Exception as e:
        print(f"Warning: Auto-scroll interrupted: {e}")


async def create_persistent_context(
    playwright_instance,
    user_data_dir: str,
    headless: bool = False,
    channel: str = "chrome"
) -> BrowserContext:
    """
    Launches a persistent browser context preserving cookies, storage, and sessions.
    """
    user_data_path = os.path.expanduser(user_data_dir)
    os.makedirs(user_data_path, exist_ok=True)

    launch_args = [
        "--disable-blink-features=AutomationControlled",
        "--no-sandbox",
        "--disable-infobars"
    ]

    # Try launching with specified channel (e.g., 'chrome')
    try:
        context = await playwright_instance.chromium.launch_persistent_context(
            user_data_dir=user_data_path,
            channel=channel,
            headless=headless,
            args=launch_args,
            viewport={"width": 1280, "height": 800},
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        )
        return context
    except Exception as e:
        print(f"Notice: Failed to launch with channel='{channel}' ({e}). Falling back to default Chromium...")
        context = await playwright_instance.chromium.launch_persistent_context(
            user_data_dir=user_data_path,
            headless=headless,
            args=launch_args,
            viewport={"width": 1280, "height": 800}
        )
        return context


async def handle_login(user_data_dir: str, login_url: str, channel: str):
    """
    Opens headed browser for manual user login. All session data will be saved.
    """
    print(f"\n[+] Opening browser for login...")
    print(f"[+] Profile directory: {user_data_dir}")
    print(f"[+] Login URL: {login_url}")

    async with async_playwright() as p:
        context = await create_persistent_context(
            p, user_data_dir=user_data_dir, headless=False, channel=channel
        )
        page = context.pages[0] if context.pages else await context.new_page()

        await page.goto(login_url)
        print("\n" + "=" * 60)
        print(" ACTION REQUIRED:")
        print(" 1. Use the opened browser window to log in to your account.")
        print(" 2. Complete any 2FA or CAPTCHAs if prompted.")
        print(" 3. Once fully logged in, come back here and press [ENTER].")
        print("=" * 60 + "\n")

        # Wait for user confirmation in terminal
        await asyncio.to_thread(input, "Press [ENTER] to save session and close browser: ")

        print("[+] Session saved successfully!")
        await context.close()


async def crawl_page(
    page: Page,
    url: str,
    output_dir: Path,
    selector: str = None,
    scroll: bool = True,
    save_format: str = "md",
    index: int = 1,
    navigate: bool = True
):
    """
    Navigates to URL (if navigate=True), extracts content, and writes to disk.
    """
    print(f"[{index}] Processing: {url}")
    if navigate:
        try:
            await page.goto(url, wait_until="networkidle", timeout=45000)
        except Exception:
            print(f"    (networkidle timed out, waiting for load event...)")
            await page.goto(url, wait_until="load", timeout=30000)

    # Optional auto-scroll for lazy-loading elements
    if scroll:
        print("    Auto-scrolling to trigger lazy content...")
        await auto_scroll(page)

    # If selector provided, wait for it
    if selector:
        try:
            await page.wait_for_selector(selector, timeout=5000)
        except Exception:
            print(f"    Warning: Selector '{selector}' not found in time, proceeding with page content.")

    # Get page HTML
    html_content = await page.content()

    # Clean and extract
    title, clean_html_content, markdown_text = clean_html(
        html_content, base_url=url, target_selector=selector
    )

    file_prefix = f"{index:03d}_{title}"

    # Save Markdown
    if save_format in ["md", "all"]:
        md_file = output_dir / f"{file_prefix}.md"
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\nSource: {url}\n\n---\n\n")
            f.write(markdown_text)
        print(f"    -> Saved Markdown: {md_file.name}")

    # Save HTML
    if save_format in ["html", "all"]:
        html_file = output_dir / f"{file_prefix}.html"
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(clean_html_content)
        print(f"    -> Saved HTML: {html_file.name}")

    # Save PDF
    if save_format in ["pdf", "all"]:
        pdf_file = output_dir / f"{file_prefix}.pdf"
        try:
            await page.pdf(path=str(pdf_file), format="A4", print_background=True)
            print(f"    -> Saved PDF: {pdf_file.name}")
        except Exception as e:
            print(f"    -> PDF generation failed (requires headless mode usually): {e}")


async def main_crawler(args):
    # Auto-enable CDP default if --active-tab is used without specifying --cdp
    if args.active_tab and not args.cdp:
        args.cdp = "http://localhost:9222"

    urls = []
    if args.url:
        if isinstance(args.url, list):
            urls.extend(args.url)
        else:
            urls.append(args.url)
    if args.file:
        file_path = Path(args.file)
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        urls.append(line)
        else:
            print(f"Error: File not found: {args.file}")
            sys.exit(1)

    if not urls and not args.active_tab:
        print("Error: No URL provided. Use --active-tab, --url <URL>, or --file <urls.txt>")
        sys.exit(1)

    base_output_dir = Path(args.output_dir)

    if args.cdp:
        print(f"[+] Connecting to existing Chrome instance via CDP at: {args.cdp}")
        async with async_playwright() as p:
            try:
                browser = await p.chromium.connect_over_cdp(args.cdp)
            except Exception as e:
                print(f"\n[!] Error connecting to Chrome via CDP ({args.cdp}): {e}")
                print("\nTo allow Playwright to access your active Chrome window:")
                print("1. Quit Google Chrome completely (Cmd + Q).")
                print("2. Re-open it from Terminal with remote debugging:")
                print('   /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222 &')
                print("   (Chrome will restore your open tabs and login sessions!)")
                print("3. Run this crawler again with: python crawler.py --active-tab\n")
                sys.exit(1)

            context = browser.contexts[0] if browser.contexts else await browser.new_context()

            # If user wants to capture the currently open tab in their window
            if args.active_tab:
                pages = context.pages
                if not pages:
                    print("Error: No open tabs found in the active Chrome instance.")
                    sys.exit(1)

                # Prioritize a tab matching any requested url or containing course keywords
                target_page = None
                if urls:
                    for p_candidate in pages:
                        if any(u in p_candidate.url for u in urls):
                            target_page = p_candidate
                            break

                if not target_page:
                    for p_candidate in reversed(pages):
                        if "courses" in p_candidate.url or "educative.io" in p_candidate.url:
                            target_page = p_candidate
                            break

                if not target_page:
                    for p_candidate in reversed(pages):
                        if p_candidate.url and not p_candidate.url.startswith("chrome://"):
                            target_page = p_candidate
                            break

                if not target_page:
                    target_page = pages[-1]

                current_url = target_page.url or (urls[0] if urls else "")
                page_title = await target_page.title()
                course_name = args.course_name or extract_course_name(current_url, page_title)

                if args.crawl_course:
                    courses_to_crawl = urls if urls else [current_url]
                    total_courses = len(courses_to_crawl)

                    for c_idx, c_url in enumerate(courses_to_crawl, start=1):
                        print(f"\n" + "#" * 65)
                        print(f" [COURSE {c_idx}/{total_courses}] {c_url}")
                        print("#" * 65 + "\n")

                        if c_url not in target_page.url:
                            print(f"[+] Navigating active tab to: {c_url}...")
                            try:
                                await target_page.goto(c_url, wait_until="networkidle", timeout=45000)
                            except Exception:
                                await target_page.goto(c_url, wait_until="load", timeout=30000)
                            await asyncio.sleep(2)

                        c_title = await target_page.title()
                        c_name = extract_course_name(target_page.url or c_url, c_title)

                        await crawl_course_hierarchy(
                            page=target_page,
                            course_name=c_name,
                            base_output_dir=base_output_dir,
                            args=args
                        )

                    print("\n[+] ALL REQUESTED COURSES HAVE BEEN DOWNLOADED AND LOCALIZED!")
                    return

                course_dir = base_output_dir / course_name
                course_dir.mkdir(parents=True, exist_ok=True)

                print(f"[+] Attached to tab: {current_url}")
                print(f"[+] Course name: {course_name}")
                print(f"[+] Target folder: {course_dir.resolve()}")

                await crawl_page(
                    page=target_page,
                    url=current_url,
                    output_dir=course_dir,
                    selector=args.selector,
                    scroll=args.scroll,
                    save_format=args.format,
                    index=1,
                    navigate=False
                )
                print(f"\n[+] Done! Content extracted from active tab into: {course_dir.resolve()}")
                return

            page = context.pages[0] if context.pages else await context.new_page()

            for idx, url in enumerate(urls, start=1):
                course_name = args.course_name or extract_course_name(url)
                course_dir = base_output_dir / course_name
                course_dir.mkdir(parents=True, exist_ok=True)

                await crawl_page(
                    page=page,
                    url=url,
                    output_dir=course_dir,
                    selector=args.selector,
                    scroll=args.scroll,
                    save_format=args.format,
                    index=idx,
                    navigate=True
                )
                if idx < len(urls):
                    print(f"    Waiting {args.delay}s before next request...")
                    await asyncio.sleep(args.delay)

            print("\n[+] Done! All downloaded content saved to:", base_output_dir.resolve())
            return

    async with async_playwright() as p:
        context = await create_persistent_context(
            p,
            user_data_dir=args.user_data_dir,
            headless=args.headless,
            channel=args.channel
        )

        page = context.pages[0] if context.pages else await context.new_page()

        for idx, url in enumerate(urls, start=1):
            course_name = args.course_name or extract_course_name(url)
            course_dir = base_output_dir / course_name
            course_dir.mkdir(parents=True, exist_ok=True)

            await crawl_page(
                page=page,
                url=url,
                output_dir=course_dir,
                selector=args.selector,
                scroll=args.scroll,
                save_format=args.format,
                index=idx,
                navigate=True
            )
            if idx < len(urls):
                print(f"    Waiting {args.delay}s before next request...")
                await asyncio.sleep(args.delay)

        await context.close()
        print("\n[+] Done! All downloaded content saved to:", base_output_dir.resolve())


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Playwright Persistent Context Web & Course Crawler (Method 3)"
    )
    parser.add_argument(
        "--active-tab",
        action="store_true",
        help="Directly scrape the currently active/focused tab in your existing Chrome window."
    )
    parser.add_argument(
        "--crawl-course",
        action="store_true",
        help="Automatically discover all chapters & lessons in the course and crawl the entire course."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-download pages even if already saved locally."
    )
    parser.add_argument(
        "--cdp",
        type=str,
        default=None,
        help="Connect to an existing running Chrome instance over CDP (e.g. http://localhost:9222)."
    )
    parser.add_argument(
        "--login",
        action="store_true",
        help="Open headed browser to log in interactively and save session state."
    )
    parser.add_argument(
        "--url",
        nargs="+",
        help="Target URL(s) to crawl or login."
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Path to a text file containing target URLs (one per line)."
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./download",
        help="Directory where downloaded content will be saved (default: ./download)."
    )
    parser.add_argument(
        "--course-name",
        type=str,
        default=None,
        help="Override course folder name (e.g. 'generative-ai-system-design')."
    )
    parser.add_argument(
        "--user-data-dir",
        type=str,
        default="./chrome_profile",
        help="Directory to store persistent Chrome profile/cookies (default: ./chrome_profile)."
    )
    parser.add_argument(
        "--channel",
        type=str,
        default="chrome",
        help="Browser channel: 'chrome' or 'chromium' (default: chrome)."
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run in headless mode (default: False for headed)."
    )
    parser.add_argument(
        "--selector",
        type=str,
        default=None,
        help="CSS selector for target content (e.g. 'article', 'main', '.course-content')."
    )
    parser.add_argument(
        "--no-scroll",
        dest="scroll",
        action="store_false",
        help="Disable auto-scrolling on pages."
    )
    parser.add_argument(
        "--format",
        choices=["md", "html", "pdf", "all"],
        default="md",
        help="Output format: md, html, pdf, or all (default: md)."
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=2.0,
        help="Delay in seconds between requests (default: 2.0)."
    )
    return parser.parse_args()


if __name__ == "__main__":
    cli_args = parse_arguments()

    if cli_args.login:
        login_target = cli_args.url or "https://www.google.com"
        asyncio.run(
            handle_login(
                user_data_dir=cli_args.user_data_dir,
                login_url=login_target,
                channel=cli_args.channel
            )
        )
    else:
        asyncio.run(main_crawler(cli_args))

