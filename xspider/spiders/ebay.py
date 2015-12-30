# -*- coding: utf-8 -*-

import scrapy
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader, Identity
# from xspider.items import EbayItem

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
    start_urls = [
        'http://www.ebay.com/sch/Cell-Phones-Smartphones-/9355/i.html',
        'http://www.ebay.com/sch/Cell-Phone-Accessories-/9394/i.html',
        'http://www.ebay.com/sch/Smart-Watches-/178893/i.html',

        'http://www.ebay.com/sch/iPads-Tablets-eBook-Readers-/171485/i.html',
        'http://www.ebay.com/sch/Cables-Connectors-/31491/i.html',
        'http://www.ebay.com/sch/Home-Networking-Connectivity-/11176/i.html',
        'http://www.ebay.com/sch/Drives-Storage-Blank-Media-/165/i.html',

        'http://www.ebay.com/sch/Portable-Audio-Headphones-/15052/i.html',
        'http://www.ebay.com/sch/Home-Automation-/50582/i.html',
        'http://www.ebay.com/sch/Home-Surveillance-/48633/i.html',
        'http://www.ebay.com/sch/Vehicle-Electronics-GPS-/3270/i.html',
        'http://www.ebay.com/sch/Multipurpose-Batteries-Power-/48446/i.html',

        'http://www.ebay.com/sch/Educational-/11731/i.html',
        'http://www.ebay.com/sch/Radio-Control-Control-Line-/2562/i.html',

        'http://www.ebay.com/sch/Cycling-/7294/i.html',
        'http://www.ebay.com/sch/Fitness-Running-Yoga-/15273/i.html',
        'http://www.ebay.com/sch/Outdoor-Sports-/159043/i.html',
    ]

    def get_category(self, url):
        if 'Cell-Phones-Smartphones-' in url:
            return 1001
        elif 'Cell-Phone-Accessories-' in url:
            return 1002
        elif 'Smart-Watches-' in url:
            return 1003
        elif 'iPads-Tablets-eBook-Readers-' in url:
            return 2001
        elif 'Cables-Connectors-' in url:
            return 2002
        elif 'Home-Networking-Connectivity-' in url:
            return 2003
        elif 'Drives-Storage-Blank-Media-' in url:
            return 2004
        elif 'Portable-Audio-Headphones-' in url:
            return 3001
        elif 'Home-Automation-' in url:
            return 3002
        elif 'Home-Surveillance-' in url:
            return 3003
        elif 'Vehicle-Electronics-GPS-' in url:
            return 3004
        elif 'Multipurpose-Batteries-Power-' in url:
            return 3005
        elif 'Educational-' in url:
            return 4001
        elif 'Radio-Control-Control-Line-' in url:
            return 4002
        elif 'Cycling-' in url:
            return 5001
        elif 'Fitness-Running-Yoga-' in url:
            return 5002
        elif 'Outdoor-Sports-' in url:
            return 5003
        return 0

    def parse(self, response):
        print('--------------------start parse---------------------')
        category = self.get_category(response.request.url)
        # 起始页
        sel = Selector(response)
        items = sel.xpath(LIST_ITEMS)
        # for index, item in enumerate(items):
        #     ebay = ItemLoader(item=EbayItem(), selector=item)
        #     ebay.add_xpath('item_id', LIST_ITEM_ID)
        #     ebay.add_xpath('url', LIST_ITEM_URL)
        #     ebay.add_xpath('title', LIST_ITEM_TITLE)
        #     ebay.add_xpath('subtitle', LIST_ITEM_SUBTITLE)
        #     ebay.add_xpath('price', LIST_ITEM_PRICE)
        #     ebay.add_xpath('price_type', LIST_ITEM_PRICE_TYPE)
        #     ebay.add_xpath('sold', LIST_ITEM_EXTRA)
        #     ebay.add_xpath('country', LIST_ITEM_COUNTRY)
        #     ebay.add_value('category', category)
        #     yield ebay.load_item()

        # 下一页
        next_page = sel.xpath(LIST_NEXT_PAGE).extract()
        print('next_page: %s' % next_page)
        if len(next_page) > 0:
            next_page_url = next_page[0]
            print('next_page_url: %s' % next_page_url)
            request = scrapy.Request(next_page_url, callback=self.parse)
            yield request

        pass
