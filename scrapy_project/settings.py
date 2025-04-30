BOT_NAME = 'localization_pro'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
ROBOTSTXT_OBEY = True
DOWNLOAD_DELAY = 2
AUTOTHROTTLE_ENABLED = True
ITEM_PIPELINES = {
    'scrapy_project.pipelines.HtmlSavePipeline': 300,
}
FEED_EXPORT_ENCODING = 'utf-8'
