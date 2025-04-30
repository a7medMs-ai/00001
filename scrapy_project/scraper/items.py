import scrapy

class LocalizationItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    language = scrapy.Field()
    word_count = scrapy.Field()
    segments = scrapy.Field()
    has_media = scrapy.Field()
