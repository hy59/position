import os
from scrapy.cmdline import execute

# os.environ['https_proxy'] = 'https://127.0.0.1:8123'
execute(['scrapy', 'crawl', 'position'])
