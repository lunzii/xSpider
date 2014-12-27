# -*- coding: utf-8 -*-
import csv
import scrapy
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader, Identity
from xspider.items import EbayItem

# 列表页数据
LIST_ITEMS = "//ul[@id='ListViewInner']/li"

# ID
LIST_ITEM_ID = "@listingid"
# LIST_ITEM_ID = "div[@class='lvpic pic p225 img left']/@iid"
# 链接
LIST_ITEM_URL = "h3[@class='lvtitle']/a/@href"
# 标题
LIST_ITEM_TITLE = "h3[@class='lvtitle']/a/node()"
# LIST_ITEM_TITLE = "h3[@class='lvtitle']/a/@title"
# 副标题
LIST_ITEM_SUBTITLE = "div[@class='lvsubtitle']/text()"
# 价格
LIST_ITEM_PRICE = "ul/li[@class='lvprice prc']/span/node()"
# 类型
LIST_ITEM_PRICE_TYPE = "ul/li[@class='lvformat bin']/span/text()"
# 红色字体
LIST_ITEM_EXTRA = "ul/li[@class='lvextras']/div/div[@class='hotness-signal red']/text()"
# 国家
LIST_ITEM_COUNTRY = "ul[@class='lvdetails left space-zero full-width']/li[not(@class)]/text()"

# 下一页
LIST_NEXT_PAGE = "//td[@class='pagn-next']/a/@href"
# LIST_NEXT_PAGE = "//a[@class='gspr next']/@href"


class EbaySpider(scrapy.Spider):
    name = "ebay"
    allowed_domains = ["ebay.com"]
    start_urls = (
        'http://www.ebay.com/sch/Cell-Phone-Accessories-/9394/i.html',
        'http://www.ebay.com/sch/Smart-Watches-/178893/i.html',
        # 'http://www.ebay.com/sch/Replacement-Parts-Tools-/43304/i.html',
        # 'http://www.ebay.com/sch/Wholesale-Lots-/45065/i.html',
        'http://www.ebay.com/sch/iPad-Tablet-eBook-Accessories-/176970/i.html',
        'http://www.ebay.com/sch/Radio-Control-Control-Line-/2562/i.html',
        'http://www.ebay.com/sch/Portable-Audio-Headphones-/15052/i.html',
        'http://www.ebay.com/sch/Laptop-Desktop-Accessories-/31530/i.html',
    )

    def parse(self, response):
        print('--------------------start parse---------------------')
        # 起始页
        sel = Selector(response)
        items = sel.xpath(LIST_ITEMS)
        for index, item in enumerate(items):
            ebay = ItemLoader(item=EbayItem(), selector=item)
            ebay.add_xpath('item_id', LIST_ITEM_ID)
            ebay.add_xpath('url', LIST_ITEM_URL)
            ebay.add_xpath('title', LIST_ITEM_TITLE)
            ebay.add_xpath('subtitle', LIST_ITEM_SUBTITLE)
            ebay.add_xpath('price', LIST_ITEM_PRICE)
            ebay.add_xpath('price_type', LIST_ITEM_PRICE_TYPE)
            ebay.add_xpath('extra', LIST_ITEM_EXTRA)
            ebay.add_xpath('country', LIST_ITEM_COUNTRY)
            yield ebay.load_item()

        # 下一页
        next_page = sel.xpath(LIST_NEXT_PAGE).extract()
        print('next_page: %s' % next_page)
        if len(next_page) > 0:
            next_page_url = next_page[0]
            print('next_page_url: %s' % next_page_url)
            request = scrapy.Request(next_page_url, callback=self.parse)
            yield request

        pass
