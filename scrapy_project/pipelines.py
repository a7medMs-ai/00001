import os
import hashlib
import re

class HtmlSavePipeline:
    def __init__(self):
        self.file_counter = {}
        
    def process_item(self, item, spider):
        # Create language directory
        lang_dir = f"output/html_pages/{item['language']}"
        os.makedirs(lang_dir, exist_ok=True)
        
        # Generate unique filename
        clean_title = re.sub(r'[^\w]', '_', item['title'])[:45]
        if not clean_title:
            clean_title = hashlib.md5(item['url'].encode()).hexdigest()[:8]
            
        if clean_title in self.file_counter:
            self.file_counter[clean_title] += 1
            filename = f"{clean_title}_{self.file_counter[clean_title]}.html"
        else:
            self.file_counter[clean_title] = 1
            filename = f"{clean_title}.html"
            
        # Save HTML content
        with open(f"{lang_dir}/{filename}", 'w', encoding='utf-8') as f:
            f.write(item['content'])
            
        return item
