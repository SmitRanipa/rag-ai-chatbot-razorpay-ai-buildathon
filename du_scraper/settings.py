from __future__ import annotations

BOT_NAME = "du_scraper"

SPIDER_MODULES = ["du_scraper.spiders"]
NEWSPIDER_MODULE = "du_scraper.spiders"

# Be a good citizen
ROBOTSTXT_OBEY = True

# Identify your crawler (put your email so site admins can reach you)
USER_AGENT = "DU-RAG-Crawler/1.0 ( DU Student 6th Sem )"

# If the site is large, avoid hammering it
CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 4
DOWNLOAD_DELAY = 0.25
RANDOMIZE_DOWNLOAD_DELAY = True
DOWNLOAD_TIMEOUT = 30

# Retries for stability (including rate-limit responses)
RETRY_TIMES = 5
RETRY_HTTP_CODES = [408, 429, 500, 502, 503, 504, 522, 524]

# AutoThrottle (recommended by Scrapy docs)
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 0.5
AUTOTHROTTLE_MAX_DELAY = 15.0
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = False

# HTTP cache speeds up dev/testing
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Pipelines (clean + normalize)
ITEM_PIPELINES = {
    "du_scraper.pipelines.CleanUniversityPagePipeline": 300,
}

# Export defaults
FEED_EXPORT_ENCODING = "utf-8"

# Helpful safety limits during early testing (comment out for full crawl)
# CLOSESPIDER_PAGECOUNT = 2000
# DEPTH_LIMIT = 8

LOG_LEVEL = "INFO"
TELNETCONSOLE_ENABLED = False

# Persist crawl state so you can stop/resume
JOBDIR = "jobs/darshan_university"

EXTENSIONS = {
    'du_scraper.extensions.ProgressExtension': 500,
}