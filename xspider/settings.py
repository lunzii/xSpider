# -*- coding: utf-8 -*-

# Scrapy settings for xspider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'xspider'

SPIDER_MODULES = ['xspider.spiders']
NEWSPIDER_MODULE = 'xspider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'

DOWNLOAD_DELAY = 2    # 1 s of delay

ITEM_PIPELINES = {
    'xspider.pipelines.ImageDownloadPipeline': 1,
    'xspider.pipelines.EbayItemPipeline': 1,
}

DATA_STORE = '/Users/olunx/Documents/spiders'

import sys
import os
sys.path.append('/Users/olunx/Documents/workspace/xTrade')
os.environ['DJANGO_SETTINGS_MODULE'] = 'xTrade.settings'
