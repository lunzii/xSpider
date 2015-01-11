# -*- coding: utf-8 -*-

import scrapy
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader
from xspider.items import AliexpressItem

# 列表页数据
LIST_ITEMS = '//*[@id="list-items"]/ul/li'

# 物品ID
LIST_ITEM_ID = '@qrdata'
# URL
LIST_ITEM_URL = 'div[@class="info"]/h3/a/@href'
# 物品名称
LIST_ITEM_TITLE = 'div[@class="info"]/h3/a/@title'
# 价格
LIST_ITEM_PRICE = 'div[@class="info"]/span[@class="price price-m"]/em[@class="value"]/text()'
# 单位
LIST_ITEM_UNIT = 'div[@class="info"]/span[@class="price price-m"]/span[@class="unit"]/text()'
# 最小订单
LIST_ITEM_MIN_ORDER = 'div[@class="info"]/p[@class="tip"]/span[@class="min-order"]/text()'
# 运费
LIST_ITEM_SHIPPING = 'div[@class="info"]/strong[@class="free-s"]/text()'
# 评价数
LIST_ITEM_RATE_NUM = 'div[@class="info"]/div[@class="rate-history"]/a[@class="rate-num "]/text()'
# 订单数
LIST_ITEM_ORDER_NUM = 'div[@class="info"]/div[@class="rate-history"]/span[@class="order-num"]/a/em/text()'
# 店铺名称
LIST_ITEM_STORE_NAME = 'div[@class="info"]/div[@class="store-name-chat"]/div[@class="store-name clearfix"]/a/@title'
# 店铺URL
LIST_ITEM_STORE_URL = 'div[@class="info"]/div[@class="store-name-chat"]/div[@class="store-name clearfix"]/a/@href'

# 下一页
LIST_NEXT_PAGE = '//*[@id="pagination-bottom"]/div[@class="pos-right"]/a[@class="page-next"]/@href'


class AliexpressSpider(scrapy.Spider):
    name = "aliexpress"
    allowed_domains = ["aliexpress.com"]
    start_urls = [
        'http://www.aliexpress.com/premium/category/200005271/1.html?shipCountry=all',
    ]

    def get_category(self, url):
        if '200005271' in url:
            return 1001
        return 0

    def parse(self, response):
        print('--------------------start parse---------------------')
        category = self.get_category(response.request.url)
        # 起始页
        sel = Selector(response)
        items = sel.xpath(LIST_ITEMS)
        for index, item in enumerate(items):
            ali = ItemLoader(item=AliexpressItem(), selector=item)
            ali.add_xpath('item_id', LIST_ITEM_ID)
            ali.add_xpath('url', LIST_ITEM_URL)
            ali.add_xpath('title', LIST_ITEM_TITLE)
            ali.add_xpath('price', LIST_ITEM_PRICE)
            ali.add_xpath('unit', LIST_ITEM_UNIT)
            ali.add_xpath('min_order', LIST_ITEM_MIN_ORDER)
            ali.add_xpath('shipping', LIST_ITEM_SHIPPING)
            ali.add_xpath('rate_num', LIST_ITEM_RATE_NUM)
            ali.add_xpath('order_num', LIST_ITEM_ORDER_NUM)
            ali.add_xpath('store_name', LIST_ITEM_STORE_NAME)
            ali.add_xpath('store_url', LIST_ITEM_STORE_URL)
            ali.add_value('category', category)
            yield ali.load_item()

        # 下一页
        next_page = sel.xpath(LIST_NEXT_PAGE).extract()
        print('next_page: %s' % next_page)
        if len(next_page) > 0:
            next_page_url = next_page[0]
            print('next_page_url: %s' % next_page_url)
            request = scrapy.Request(next_page_url, callback=self.parse)
            yield request

        pass
