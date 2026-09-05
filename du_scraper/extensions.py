import time
from scrapy import signals

class ProgressExtension:
    def __init__(self):
        self.start_time = None
        self.pages_scraped = 0
        self.total_requests = 0

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        return ext

    def spider_opened(self, spider):
        self.start_time = time.time()
        # Try to estimate total requests from settings if available
        self.total_requests = spider.crawler.settings.get('CLOSESPIDER_PAGECOUNT', None)
        spider.logger.info("Crawl started at %s", time.ctime(self.start_time))
        if self.total_requests:
            spider.logger.info(f"Estimated total pages: {self.total_requests}")

    def item_scraped(self, item, spider):
        self.pages_scraped += 1
        elapsed = time.time() - self.start_time
        rate = self.pages_scraped / elapsed if elapsed > 0 else 0

        # ETA calculation
        if self.total_requests and rate > 0:
            remaining = (self.total_requests - self.pages_scraped) / rate
            percent = (self.pages_scraped / self.total_requests) * 100
        else:
            remaining = None
            percent = None

        # Format ETA
        if remaining is not None:
            hrs, rem = divmod(int(remaining), 3600)
            mins, secs = divmod(rem, 60)
            eta_str = f"{hrs}h {mins}m {secs}s"
        else:
            eta_str = "Unknown"

        pct_str = f"{percent:.2f}%" if percent is not None else "Unknown"

        spider.logger.info(
            f"[Progress] Pages: {self.pages_scraped} | Rate: {rate:.2f} pages/sec | "
            f"Elapsed: {int(elapsed)}s | ETA: {eta_str} | Completed: {pct_str}"
        )

    def spider_closed(self, spider, reason):
        elapsed = time.time() - self.start_time
        spider.logger.info(f"Crawl finished after {int(elapsed)}s with {self.pages_scraped} pages scraped. Reason: {reason}")