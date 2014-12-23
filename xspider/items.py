# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class MeizituItem(scrapy.Item):
    title = scrapy.Field()
    tags = scrapy.Field()
    url = scrapy.Field()
    day = scrapy.Field()
    month_year = scrapy.Field()
    image_urls = scrapy.Field()
