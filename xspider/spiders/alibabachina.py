# -*- coding: utf-8 -*-

import scrapy
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader
from xspider.items import AlibabaChinaItem

# 列表页数据
LIST_ITEMS = '//*[@id="sw_maindata_asyncload"]/li'

# 物品ID
LIST_ITEM_ID = '@offerid'
# 物品名称
LIST_ITEM_TITLE = 'h2[@class="sm-offerShopwindow-title"]/a[@class="sm-offerShopwindow-titleLink sw-ui-font-title12"]/text()'
# 公司ID
LIST_ITEM_COMPANY_ID = '@companyid'
# 公司名
LIST_ITEM_COMPANY_NAME = 'div[@class="sm-offerShopwindow-company fd-clr"]/a[@class="sm-previewCompany sw-mod-previewCompanyInfo"]/text()'
# 公司链接
LIST_ITEM_COMPANY_URL = 'div[@class="sm-offerShopwindow-company fd-clr"]/a[@class="sm-previewCompany sw-mod-previewCompanyInfo"]/@href'
# 公司所在地
LIST_ITEM_COMPANY_LOCATION = 'div[@class="sm-offerShopwindow-summary fd-clr"]/*[@class="sm-offerShopwindow-summary-place"]/text()'
# 卖出数量
LIST_ITEM_SOLD_ITEM = 'div[@class="sm-offerShopwindow-price"]/span[@class="sm-offerShopwindow-trade"]/em[1]/text()'
# 购买人数
LIST_ITEM_SOLD_PERSON = 'div[@class="sm-offerShopwindow-price"]/span[@class="sm-offerShopwindow-trade"]/em[2]/text()'
# 价钱
LIST_ITEM_PRICE = 'div[@class="sm-offerShopwindow-price"]/span[@class="su-price"]/text()'

# 下一页
LIST_NEXT_PAGE = '//*[@id="sw_mod_pagination_content"]/div/a[@class="page-next"]/@href'


class AlibabachinaSpider(scrapy.Spider):
    name = "alibabachina"
    allowed_domains = ["1688.com"]

    start_urls = [
        'http://s.1688.com/selloffer/--7.html?pageSize=20&quantityBegin=1',
    ]

    def get_category(self, url):
        if '--7.html' in url:
            return 1001

    def parse(self, response):
        print('--------------------start parse---------------------')
        category = self.get_category(response.request.url)
        # 起始页
        sel = Selector(response)
        items = sel.xpath(LIST_ITEMS)
        for index, item in enumerate(items):
            ali = ItemLoader(item=AlibabaChinaItem(), selector=item)
            ali.add_xpath('item_id', LIST_ITEM_ID)
            ali.add_xpath('title', LIST_ITEM_TITLE)
            ali.add_xpath('company_id', LIST_ITEM_COMPANY_ID)
            ali.add_xpath('company_name', LIST_ITEM_COMPANY_NAME)
            ali.add_xpath('company_url', LIST_ITEM_COMPANY_URL)
            ali.add_xpath('company_location', LIST_ITEM_COMPANY_LOCATION)
            ali.add_xpath('price', LIST_ITEM_PRICE)
            ali.add_xpath('sold_item', LIST_ITEM_SOLD_ITEM)
            ali.add_xpath('sold_person', LIST_ITEM_SOLD_PERSON)
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


