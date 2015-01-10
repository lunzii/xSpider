# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.contrib.djangoitem import DjangoItem
from apps.ebay.models import EbayStuff
from apps.alibabachina.models import AlibabaChinaStuff

class XspiderItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass


class MeizituItem(Item):
    title = Field()
    tags = Field()
    url = Field()
    day = Field()
    month_year = Field()
    image_urls = Field()

# class EbayItem(Item):
#     item_id = Field()
#     url = Field()
#     title = Field()
#     subtitle = Field()
#     price = Field()
#     price_type = Field()
#     extra = Field()
#     country = Field()


class EbayItem(DjangoItem):
    django_model = EbayStuff


class AlibabaChinaItem(DjangoItem):
    django_model = AlibabaChinaStuff
