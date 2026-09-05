import re
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from du_scraper.utils.extract import extract_main_html, html_to_text, compute_hash, looks_bad


DENY_EXTENSIONS = re.compile(
    r".*\.(jpg|jpeg|png|gif|webp|svg|css|js|ico|zip|rar|7z|mp4|mp3|avi|mov|pdf|doc|docx|xls|xlsx)$",
    re.IGNORECASE,
)


def detect_page_type(url: str) -> str:
    url = url.lower()

    if "placement" in url:
        return "placement"
    if "department" in url:
        return "department"
    if "course" in url or "program" in url:
        return "course"
    if "faculty" in url:
        return "faculty"

    return "general"


class DarshanSpider(CrawlSpider):
    name = "darshan"
    allowed_domains = ["darshan.ac.in"]

    def __init__(self, start_urls=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if start_urls:
            self.start_urls = start_urls.split(",")
        else:
            self.start_urls = [
                "https://darshan.ac.in/",
                "https://darshan.ac.in/sitemap",
                "https://darshan.ac.in/placement/list",
            ]

    rules = (
        Rule(
            LinkExtractor(
                allow_domains=["darshan.ac.in"],
                deny=(
                    r"/Login",
                    r"/logout",
                    r"/search",
                    r"/Content/",
                    r"/assets/",
                ),
                unique=True,
            ),
            callback="parse_page",
            follow=True,
        ),
    )

    custom_settings = {
        "ROBOTSTXT_OBEY": True,
        "DOWNLOAD_DELAY": 0.25,
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_START_DELAY": 0.25,
        "AUTOTHROTTLE_MAX_DELAY": 5.0,
        "CONCURRENT_REQUESTS": 8,
        "RETRY_TIMES": 3,
        "HTTPCACHE_ENABLED": True,
        "FEED_EXPORT_ENCODING": "utf-8",
    }

    def parse_page(self, response: scrapy.http.Response):
        url = response.url.split("#")[0]

        # Skip obvious binaries
        if DENY_EXTENSIONS.match(url):
            return

        # Remove unwanted page elements
        for selector in ["nav", "header", "footer", "script", "style"]:
            for el in response.css(selector):
                el.root.getparent().remove(el.root)

        title = (response.css("title::text").get() or "").strip()

        meta_desc = (
            response.css('meta[name="description"]::attr(content)').get() or ""
        ).strip()

        canonical = response.css('link[rel="canonical"]::attr(href)').get()
        canonical_url = canonical.strip() if canonical else url

        headings = [
            h.strip()
            for h in response.css("h1::text, h2::text, h3::text").getall()
            if h.strip()
        ]

        raw_html = response.text

        main_html = extract_main_html(raw_html)
        text = html_to_text(main_html)

        internal_links = response.css("a::attr(href)").getall()

        item = {
            "url": url,
            "canonical_url": canonical_url,
            "title": title,
            "meta_description": meta_desc,
            "headings": headings,
            "page_type": detect_page_type(url),
            "text": text,
            "text_length": len(text or ""),
            "content_hash": compute_hash(text or ""),
            "internal_links": internal_links[:50],
            "scraped_at": response.headers.get("Date", b"").decode(
                "utf-8", errors="ignore"
            ),
            "main_html": main_html,
            "raw_html": raw_html,
        }

        # Skip very bad pages if needed
        # if looks_bad(text):
        #     return

        yield item


#         Run Command (PowerShell)
# Crawl whole website
# scrapy crawl darshan -O data/raw/pages.jsonl
# Crawl only placement pages
# scrapy crawl darshan -a start_urls=https://darshan.ac.in/placement/list -O data/raw/placement_pages.jsonl
# Your Next Step for RAG Pipeline

# After crawling: