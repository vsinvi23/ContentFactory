# Playwright Persistent Context Crawler (Method 3)

A Python crawler powered by Playwright that preserves your authenticated session (cookies, storage, auth tokens) in a dedicated persistent Chrome context. Designed for downloading and saving course materials and web pages into clean **Markdown**, **HTML**, or **PDF**.

---

## Features

- **Persistent Authentication**: Log in once interactively; cookies and sessions are preserved in `./chrome_profile`.
- **Method 3 Persistent Context**: Uses Playwright's `launch_persistent_context` directly with installed Google Chrome (`channel="chrome"`).
- **Auto-Scrolling**: Automatically scrolls down pages to trigger lazy-loaded images, interactive diagrams, and deferred code blocks before capturing DOM.
- **Content Cleaning & Markdown Conversion**: Strips ads, scripts, navbars, and headers; converts clean content into GitHub-flavored Markdown.
- **Batch Processing**: Feed a list of lesson/chapter URLs from a text file.
- **Multiple Formats**: Export to `.md`, `.html`, `.pdf`, or `all`.

---

## Quickstart

### 1. Activate Environment

The virtual environment `.venv` is already configured in this workspace:
```bash
source .venv/bin/activate
```

*(If setting up on a new machine, install dependencies with: `pip install -r requirements.txt && playwright install`)*

---

### 2. Step 1: Log in once (One-time Setup)

Run the crawler with the `--login` flag and provide the login page:

```bash
python crawler.py --login --url "https://educative.io/login"
```

1. A Google Chrome window will launch.
2. Log in with your email, password, or Google/GitHub SSO.
3. Complete any two-factor authentication (2FA).
4. Once you are successfully logged in and see your dashboard, return to the terminal and press **`[ENTER]`**.
5. Your authenticated session is permanently stored in `./chrome_profile`.

---

### 3. Step 2: Download / Crawl Content

#### Download a Single Page / Chapter
```bash
python crawler.py --url "https://educative.io/courses/YOUR_COURSE/LESSON_1" --format md
```

#### Download Multiple Lessons (Batch Mode)
1. Add URLs to a text file (e.g. `urls.txt`):
   ```text
   https://educative.io/courses/YOUR_COURSE/module-1
   https://educative.io/courses/YOUR_COURSE/module-2
   https://educative.io/courses/YOUR_COURSE/module-3
   ```
2. Run the crawler:
   ```bash
   python crawler.py --file urls.txt --output-dir ./my_course --format all
   ```

Files are numbered and saved in `./my_course/` (e.g., `001_Introduction.md`, `002_Module_1.md`).

---

## If You Are Already Logged In On Chrome

You have two simple ways to use your active Chrome login:

### Option A: Connect directly to your running Chrome (Zero re-login)

Start Chrome with remote debugging enabled so Playwright can attach directly to your open tabs and active login session:

1. Close Chrome completely (`Cmd + Q`).
2. Run this command in Terminal to start Chrome with debugging enabled:
   ```bash
   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 &
   ```
3. Your regular Chrome will open with all your bookmarks, extensions, and logged-in profiles.
4. Run the crawler using `--cdp`:
   ```bash
   python crawler.py --cdp http://localhost:9222 --url "https://educative.io/courses/YOUR_COURSE/LESSON_1"
   ```

---

### Option B: Use your Chrome Profile Directory Directly (Chrome Closed)

If you don't want to use `--remote-debugging-port`, Playwright can open your existing profile directly:

1. **Quit Google Chrome (`Cmd + Q`)** so the database lock is released.
2. Run the crawler pointing to your profile:
   ```bash
   python crawler.py \
     --user-data-dir "$HOME/Library/Application Support/Google/Chrome" \
     --url "https://educative.io/courses/YOUR_COURSE/LESSON_1"
   ```

---

## Command Reference

| Flag | Description | Default |
|------|-------------|---------|
| `--login` | Launches headed browser to log in interactively and save session | `False` |
| `--url <URL>` | Single URL to scrape or login | `None` |
| `--file <PATH>` | Text file containing URLs (one per line) | `None` |
| `--format` | Output format: `md`, `html`, `pdf`, `all` | `md` |
| `--output-dir` | Output folder for extracted content | `./downloads` |
| `--user-data-dir` | Folder storing Chrome profile & session data | `./chrome_profile` |
| `--channel` | Browser binary channel (`chrome` or `chromium`) | `chrome` |
| `--selector` | CSS selector for main article container | Auto-detect |
| `--no-scroll` | Disable auto-scroll before capturing | Scroll enabled |
| `--delay` | Delay in seconds between requests | `2.0` |
| `--headless` | Run in headless mode without a visible window | `False` |

