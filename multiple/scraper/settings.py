# -*- coding: utf-8 -*-

# Scrapy settings for xSpider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

# 添加Django支持
import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "xspider.settings")


# Scrapy 配置
BOT_NAME = 'multiple'

SPIDER_MODULES = ['dynamic_scraper.spiders', 'multiple.spiders']
NEWSPIDER_MODULE = 'multiple.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'

DOWNLOAD_DELAY = 2    # 2s of delay

ITEM_PIPELINES = {
    'dynamic_scraper.pipelines.ValidationPipeline': 400,
    'app.scraper.pipelines.ImageDownloadPipeline': 1,
}

# 文件存储
DATA_STORE = '/Users/olunx/Documents/spiders'
