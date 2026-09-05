import scrapy


class UniversityPageItem(scrapy.Item):
    url = scrapy.Field()
    canonical_url = scrapy.Field()

    title = scrapy.Field()
    meta_description = scrapy.Field()
    breadcrumbs = scrapy.Field()
    headings = scrapy.Field()

    raw_html = scrapy.Field()
    main_html = scrapy.Field()
    text = scrapy.Field()
    text_length = scrapy.Field()

    scraped_at = scrapy.Field()
    content_hash = scrapy.Field()