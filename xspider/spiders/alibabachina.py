# -*- coding: utf-8 -*-

import scrapy
from scrapy.selector import Selector, HtmlXPathSelector
from scrapy.contrib.loader import ItemLoader, Identity
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from xspider.items import AlibabachinaItem

# Title
ITEM_TITLE = '//*[@id="mod-detail-title"]/h1/text()'
ITEM_PRICE = '//*[@id="mod-detail-price"]/div/table/tr[@class="price"]/td[2]/node()'
ITEM_LOCATION = '//*[@id="mod-detail-bd"]/div[2]/div[6]/div/div/div[2]/div[1]/p[1]/span/text()'
ITEM_SHIPPING = '//*[@id="mod-detail-bd"]/div[2]/div[6]/div/div/div[2]/div[2]/div/div/div/node()'
ITEM_CONTENT = '//*[@id="desc-lazyload-container"]/@data-tfs-url'
ITEM_IMAGE = '//img/@src'


class AlibabachinaSpider(scrapy.Spider):
    name = "alibabachina"
    allowed_domains = ["1688.com"]

    def __init__(self, **kw):
        super(AlibabachinaSpider, self).__init__(**kw)
        url = kw.get('url') or kw.get('page')
        print('AlibabachinaSpider url: %s' % url)
        if url and not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://%s/' % url
        else:
            url = 'http://detail.1688.com/offer/42326799135.html'
        self.url = url
        # self.allowed_domains = [urlparse(url).hostname.lstrip('www.')]
        self.link_extractor = SgmlLinkExtractor()
        # self.cookies_seen = set()

    def start_requests(self):
        return [scrapy.Request(self.url, callback=self.parse)]

    def parse(self, response):
        sel = Selector(response)
        alibaba = ItemLoader(item=AlibabachinaItem(), selector=sel)
        alibaba.add_value('url', self.url)
        alibaba.add_xpath('title', ITEM_TITLE)
        alibaba.add_xpath('price', ITEM_PRICE)
        alibaba.add_xpath('location', ITEM_LOCATION)
        alibaba.add_xpath('shipping', ITEM_SHIPPING)
        alibaba.add_xpath('content_url', ITEM_CONTENT)
        yield alibaba.load_item()

