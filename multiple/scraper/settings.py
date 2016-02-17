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

SPIDER_MODULES = ['dynamic_scraper.spiders', 'multiple.scraper']

# Crawl responsibly by identifying yourself (and your website) on the user-agent

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'


DSCRAPER_LOG_ENABLED = True
DSCRAPER_LOG_LEVEL = 'INFO'
DSCRAPER_LOG_LIMIT = 5
DOWNLOAD_DELAY = 2    # 2s of delay

ITEM_PIPELINES = {
    'dynamic_scraper.pipelines.DjangoImagesPipeline': 200,
    'dynamic_scraper.pipelines.ValidationPipeline': 400,
    'multiple.scraper.pipelines.CocoaControlsPipeline': 800,
}

# 文件存储
DATA_STORE = os.path.join(PROJECT_ROOT, '../files')
IMAGES_STORE = os.path.join(PROJECT_ROOT, '../thumbnails')
