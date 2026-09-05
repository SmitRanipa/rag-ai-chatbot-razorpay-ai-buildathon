from __future__ import annotations

import hashlib
import re
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from bs4 import BeautifulSoup
from readability import Document
from w3lib.url import canonicalize_url


_WHITESPACE_RE = re.compile(r"[ \t]+")
_MULTI_NL_RE = re.compile(r"\n{3,}")


def _clean_text(text: str) -> str:
    # Normalize newlines
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Remove trailing spaces per line
    lines = [ln.strip() for ln in text.split("\n")]
    # Drop empty lines and very short junk lines
    lines = [ln for ln in lines if ln and len(ln) > 1]
    text = "\n".join(lines)
    # Collapse multiple spaces
    text = _WHITESPACE_RE.sub(" ", text)
    # Collapse too many blank lines
    text = _MULTI_NL_RE.sub("\n\n", text)
    return text.strip()


def _html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")

    # Remove typical non-content elements (defense-in-depth)
    for tag in soup(["script", "style", "noscript", "svg", "form", "nav", "footer", "header", "aside"]):
        tag.decompose()

    text = soup.get_text("\n", strip=True)
    return _clean_text(text)


class CleanUniversityPagePipeline:
    """
    Produces:
      - canonical_url
      - main_html (readability)
      - text (clean)
      - content_hash
      - scraped_at
    """

    def process_item(self, item: Dict[str, Any], spider):
        url = item.get("url") or ""
        item["canonical_url"] = canonicalize_url(url, keep_fragments=False)

        raw_html = item.get("raw_html") or ""
        item["scraped_at"] = datetime.now(timezone.utc).isoformat()

        main_html: Optional[str] = None
        if raw_html:
            try:
                doc = Document(raw_html)
                main_html = doc.summary(html_partial=True)
            except Exception:
                main_html = None

        item["main_html"] = main_html or ""

        # Text extraction prefers main_html; fallback to whole page
        html_for_text = main_html if main_html else raw_html
        item["text"] = _html_to_text(html_for_text) if html_for_text else ""
        item["text_length"] = len(item["text"])

        # Stable hash for change detection
        h = hashlib.sha256()
        h.update(item["canonical_url"].encode("utf-8", errors="ignore"))
        h.update(b"\n")
        h.update(item["text"].encode("utf-8", errors="ignore"))
        item["content_hash"] = h.hexdigest()

        # Optional: drop ultra-small pages (menus, empty, etc.)
        if item["text_length"] < 200 and "/placement/list/" not in item["canonical_url"]:
            raise spider.DropItem(f"Too little content: {item['canonical_url']}")

        return item