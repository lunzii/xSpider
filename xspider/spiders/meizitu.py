# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader, Identity
from xspider.items import MeizituItem

# 列表页
LIST_NEXT_PAGE_TITLE = u'下一页'
LIST_NEXT_PAGE = '//*[@id="wp_page_numbers"]/ul/li/a[text()="%s"]/@href' % LIST_NEXT_PAGE_TITLE

LIST_URLS = '//*[@id="maincontent"]/div[1]/ul/li'
LIST_URL_ITEM = 'div/div/a/@href'

# 详情页面
ITEM_TITLE = '//*[@id="maincontent"]/div[1]/div[1]/h2/a/text()'
ITEM_TAGS = '//*[@id="maincontent"]/div[1]/div[1]/p/text()'
ITEM_DAY = "//div[@class='metaLeft']/div[@class='day']/text()"
ITEM_MONTH_YEAR = "//div[@class='metaLeft']/div[@class='month_Year']/text()"
ITEM_IMAGE_URLS = '//*[@class="postContent"]/p/img/@src'


class MeizituSpider(scrapy.Spider):
    name = "meizitu"
    allowed_domains = ['meizitu.com']
    start_urls = (
        'http://www.meizitu.com/a/list_1_1.html',
    )

    def parse(self, response):
        print('--------------------start parse---------------------')

        # 起始页
        sel = Selector(response)
        for url in sel.xpath(LIST_URLS):
            url = url.xpath(LIST_URL_ITEM).extract()
            print('url: %s' % url[0])
            print('------------------------------------------------')
            request = scrapy.Request(url[0], callback=self._parse_item)
            yield request

        # 下一页
        next_page = sel.xpath(LIST_NEXT_PAGE).extract()
        print('next_page: %s' % next_page)
        if len(next_page) > 0:
            next_page_url = 'http://www.meizitu.com/a/%s' % next_page[0]
            print('next_page_url: %s' % next_page_url)
            request = scrapy.Request(next_page_url, callback=self.parse)
            yield request

        print('---------------------end parse----------------------')
        pass

    def _parse_item(self, response):
        print('--------------------start item : %s' % response.url)
        item = ItemLoader(item=MeizituItem(), response=response)
        item.add_xpath('title', ITEM_TITLE)
        item.add_xpath('tags', ITEM_TAGS)
        item.add_value('url', response.url)
        item.add_xpath('day', ITEM_DAY)
        item.add_xpath('month_year', ITEM_MONTH_YEAR)
        item.add_xpath('image_urls', ITEM_IMAGE_URLS)
        return item.load_item()
