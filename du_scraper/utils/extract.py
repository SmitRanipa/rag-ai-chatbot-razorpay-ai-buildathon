import re
from html import unescape
from hashlib import sha256

from ftfy import fix_text
from w3lib.html import remove_tags, remove_tags_with_content

# Optional but strong extractors
try:
    from readability import Document
except Exception:
    Document = None

try:
    import trafilatura
except Exception:
    trafilatura = None


_WHITESPACE_RE = re.compile(r"\s+")
_BOILER_RE = re.compile(
    r"(all rights reserved|darshan university|contact us|terms|sitemap|follow us)",
    re.IGNORECASE,
)

def normalize_text(text: str) -> str:
    text = unescape(text or "")
    text = fix_text(text)
    text = text.replace("\u00a0", " ")
    text = _WHITESPACE_RE.sub(" ", text).strip()
    return text

def extract_main_html(raw_html: str) -> str:
    """Return a best-effort main-content HTML snippet."""
    if not raw_html:
        return ""

    # 1) Trafilatura (often best for main content)
    if trafilatura is not None:
        try:
            downloaded = trafilatura.extract(
                raw_html,
                include_comments=False,
                include_tables=True,
                include_links=False,
                output_format="html",
            )
            if downloaded and len(downloaded) > 200:
                return downloaded
        except Exception:
            pass

    # 2) Readability-lxml fallback
    if Document is not None:
        try:
            doc = Document(raw_html)
            summary = doc.summary(html_partial=True)
            if summary and len(summary) > 200:
                return summary
        except Exception:
            pass

    # 3) Last fallback: remove scripts/styles and return body-ish
    cleaned = remove_tags_with_content(raw_html, ("script", "style", "noscript"))
    return cleaned

def html_to_text(main_html: str) -> str:
    if not main_html:
        return ""
    # remove script/style remnants if any
    main_html = remove_tags_with_content(main_html, ("script", "style", "noscript"))
    text = remove_tags(main_html)
    text = normalize_text(text)

    # Drop ultra-boilerplate-only pages
    if len(text) < 120:
        return text

    return text

def compute_hash(text: str) -> str:
    return sha256((text or "").encode("utf-8")).hexdigest()

def looks_bad(text: str, url: str = "") -> bool:
    """Heuristic: too short or mostly boilerplate."""
    if "/placement/list/" in url:
        return False
    if not text:
        return True
    if len(text) < 300:
        return True
    # if boilerplate keywords dominate
    hits = len(_BOILER_RE.findall(text))
    return hits >= 3 and len(text) < 800