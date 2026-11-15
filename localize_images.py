#!/usr/bin/env python3
"""
Downloads all remote images referenced in markdown files and rewrites links to local relative paths.
Guarantees full offline viewing capability even if Educative is down or unreachable.
"""

import os
import re
import sys
import hashlib
import urllib.request
import urllib.parse
from pathlib import Path


def get_extension_from_headers(content_type: str, url: str) -> str:
    ct = content_type.lower()
    if "svg" in ct:
        return ".svg"
    elif "png" in ct:
        return ".png"
    elif "jpeg" in ct or "jpg" in ct:
        return ".jpg"
    elif "webp" in ct:
        return ".webp"
    elif "gif" in ct:
        return ".gif"
    
    # Try getting from path
    parsed = urllib.parse.urlparse(url)
    ext = os.path.splitext(parsed.path)[1].lower()
    if ext in [".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif"]:
        return ext
    return ".png"


def download_image(url: str, dest_dir: Path) -> str:
    """
    Downloads an image from a URL, saves it to dest_dir, and returns the local relative filename.
    """
    dest_dir.mkdir(parents=True, exist_ok=True)

    # Generate a stable hash-based filename from URL
    url_clean = url.split("?")[0] if "?" in url else url
    url_hash = hashlib.md5(url.encode("utf-8")).hexdigest()[:12]

    # Guess extension initially or fetch headers
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            )
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            content_type = response.headers.get("Content-Type", "")
            ext = get_extension_from_headers(content_type, url)
            filename = f"img_{url_hash}{ext}"
            file_path = dest_dir / filename

            if not file_path.exists() or file_path.stat().st_size == 0:
                with open(file_path, "wb") as f:
                    f.write(response.read())
            return filename
    except Exception as e:
        print(f"      [!] Failed to download image {url[:60]}...: {e}")
        return ""


def is_lesson_content_image(url: str) -> bool:
    """
    Ensures the image belongs strictly to the lesson content
    (system design diagrams, flowcharts, architectures) and not generic
    site assets like avatars, logos, badges, or analytics trackers.
    """
    url_lower = url.lower()
    # Filter out common UI assets and trackers
    skip_keywords = [
        "avatar", "favicon", "logo", "badge", "tracker",
        "google-analytics", "facebook.com", "hotjar",
        "user_profile", "gravatar", "thumb", "rating", "star"
    ]
    if any(k in url_lower for k in skip_keywords):
        return False
    return True


def process_markdown_file(md_path: Path):
    """
    Scans a markdown file, downloads all images to a dedicated folder specific
    only to that lesson (<lesson_name>_images/), and rewrites links so the lesson
    is completely self-contained.
    """
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Clean up empty data:image/svg+xml responsive placeholders that precede real images
    content = re.sub(r'!\[\]\(data:image/svg\+xml,[^)]+\)', '', content)

    # Pattern for markdown images: ![alt](url "title") or ![alt](url)
    img_pattern = re.compile(r'!\[([^\]]*)\]\((https?://[^\s\)]+)(?:\s+"([^"]*)")?\)')

    # Create a dedicated image directory strictly for THIS lesson
    lesson_folder_name = f"{md_path.stem}_images"
    lesson_images_dir = md_path.parent / lesson_folder_name
    downloaded_count = 0

    def replacer(match):
        nonlocal downloaded_count
        alt = match.group(1)
        url = match.group(2)
        title = match.group(3)

        # Ensure the image is relevant to this lesson
        if not is_lesson_content_image(url):
            return ""

        local_filename = download_image(url, lesson_images_dir)
        if local_filename:
            downloaded_count += 1
            local_rel_path = f"{lesson_folder_name}/{local_filename}"
            if title:
                return f'![{alt}]({local_rel_path} "{title}")'
            return f'![{alt}]({local_rel_path})'
        return match.group(0)

    updated_content = img_pattern.sub(replacer, content)

    if downloaded_count > 0:
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print(f"    -> Localized {downloaded_count} image(s) for lesson: {md_path.name} -> {lesson_folder_name}/")


def localize_all_course_images(course_dir: Path):
    print(f"\n[+] Scanning and localizing all images in: {course_dir.resolve()}...")
    md_files = sorted(course_dir.glob("**/*.md"))
    total_files = len(md_files)
    print(f"[+] Found {total_files} markdown files to process.")

    for idx, md_path in enumerate(md_files, start=1):
        if md_path.name == "INDEX.md":
            continue
        process_markdown_file(md_path)

    print("\n[+] All images have been downloaded locally and linked!")


if __name__ == "__main__":
    target_path = Path("./download/generative-ai-system-design")
    if len(sys.argv) > 1:
        target_path = Path(sys.argv[1])
    localize_all_course_images(target_path)

