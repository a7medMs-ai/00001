import scrapy
from urllib.parse import urlparse
import os
import hashlib
from ..items import LocalizationItem

class AdvancedSpider(scrapy.Spider):
    name = "professional_crawler"
    custom_settings = {
        'DEPTH_LIMIT': 5,
        'CONCURRENT_REQUESTS': 3
    }

    def __init__(self, url, languages=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [url]
        self.allowed_domains = [urlparse(url).netloc]
        self.languages = languages or ['en']
        self.visited_urls = set()
        self.file_counter = {}

    def parse(self, response):
        # تجنب الزيارات المكررة
        url_hash = hashlib.md5(response.url.encode()).hexdigest()
        if url_hash in self.visited_urls:
            return
        self.visited_urls.add(url_hash)

        # استخراج البيانات الأساسية
        item = LocalizationItem()
        item['url'] = response.url
        item['title'] = response.css('title::text').get(default='').strip()[:255]
        item['content'] = self.clean_content(response.css('body').get())
        item['language'] = self.detect_language(response)
        item['has_media'] = self.has_media(response)
        item['word_count'] = self.count_words(item['content'])
        item['segments'] = self.count_segments(item['content'])

        # حفظ HTML مع اسم فريد
        self.save_html(response.text, item)
        
        yield item

        # متابعة الروابط الداخلية
        for link in response.css('a::attr(href)').getall():
            yield response.follow(link, callback=self.parse)

    def clean_content(self, raw_html):
        # إزالة الأكواد غير الضرورية
        cleaned = re.sub(r'<script\b[^>]*>.*?</script>', '', raw_html, flags=re.DOTALL)
        cleaned = re.sub(r'<style\b[^>]*>.*?</style>', '', cleaned, flags=re.DOTALL)
        return cleaned.strip()

    def save_html(self, content, item):
        # تنظيم الملفات حسب اللغة
        lang_dir = f"output/html_pages/{item['language']}"
        os.makedirs(lang_dir, exist_ok=True)
        
        # إنشاء اسم ملف فريد
        base_name = re.sub(r'\W+', '_', item['title'])[:50] or 'page'
        if base_name in self.file_counter:
            self.file_counter[base_name] += 1
            filename = f"{base_name}_{self.file_counter[base_name]}.html"
        else:
            self.file_counter[base_name] = 1
            filename = f"{base_name}.html"
        
        with open(f"{lang_dir}/{filename}", 'w', encoding='utf-8') as f:
            f.write(content)

    def detect_language(self, response):
        # كشف اللغة من الـ HTML
        lang = response.css('html::attr(lang)').get()
        if lang and lang[:2] in self.languages:
            return lang[:2]
        return self.languages[0]

    def count_words(self, text):
        # حساب الكلمات بدقة للعربية والإنجليزية
        return len(re.findall(r'\b\w+[\u0600-\u06FF]+\b|\b\w+\b', text))

    def count_segments(self, text):
        # حساب السجمنتات بناء على الفقرات
        return text.count('\n\n') + 1

    def has_media(self, response):
        # التحقق من وجود وسائط
        return bool(response.css('img, video, audio, iframe'))
