"""
Content extractor and cleaner for converting web pages into clean Markdown and HTML.
"""

from bs4 import BeautifulSoup
from markdownify import markdownify as md
import re
from urllib.parse import urljoin


def clean_html(html_content: str, base_url: str = "", target_selector: str = None) -> tuple[str, str, str]:
    """
    Cleans HTML and returns:
    - title: extracted or sanitized title of the document
    - cleaned_html: HTML with unwanted tags removed and relative URLs fixed
    - markdown: converted clean markdown
    """
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract title
    title = ""
    if soup.title and soup.title.string:
        title = soup.title.string.strip()
    elif soup.find("h1"):
        title = soup.find("h1").get_text(strip=True)
    else:
        title = "untitled_page"

    # Sanitize title for filename
    clean_title = re.sub(r'[\\/*?:"<>|]', "", title)
    clean_title = re.sub(r"\s+", "_", clean_title)[:80]

    # Select target container if provided
    selected_node = None
    if target_selector:
        selected_node = soup.select_one(target_selector)

    # Fallback to common main content containers if selector not found or not provided
    if not selected_node:
        for selector in ["article", "main", "[role='main']", "#content", ".content", ".course-content", "body"]:
            selected_node = soup.select_one(selector)
            if selected_node:
                break

    if not selected_node:
        selected_node = soup

    # Remove non-content tags
    for tag in selected_node(["script", "style", "noscript", "iframe", "svg", "button", "nav", "footer", "header"]):
        tag.decompose()

    # Convert relative links and images to absolute
    if base_url:
        for img in selected_node.find_all("img", src=True):
            img["src"] = urljoin(base_url, img["src"])
        for a in selected_node.find_all("a", href=True):
            a["href"] = urljoin(base_url, a["href"])

    cleaned_html = str(selected_node)

    # Convert to Markdown
    markdown_text = md(
        cleaned_html,
        heading_style="ATX",
        bullets="-",
        strip=["script", "style"]
    )

    # Clean up extra newlines in markdown
    markdown_text = re.sub(r"\n{3,}", "\n\n", markdown_text).strip()

    return clean_title, cleaned_html, markdown_text

