# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import requests
from bs4 import BeautifulSoup
from django.db import IntegrityError
from scrapy.selector import Selector

from xspider import settings


class ImageDownloadPipeline(object):
    def process_item(self, item, spider):
        if spider.name not in ['meizitu']:
            return item
        print('---------------------ImageDownloadPipeline ----------------------')
        if 'image_urls' in item:
            dir_path = '%s/%s' % (settings.DATA_STORE, spider.name)

            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

            for image_url in item['image_urls']:
                print('---------------------download image: %s' % image_url)
                url = image_url.split('/')
                file_path = '%s/%s_%s_%s_%s' % (dir_path, url[-4], url[-3], url[-2], url[-1])
                if os.path.exists(file_path):
                    continue
                with open(file_path, 'wb') as handle:
                    response = requests.get(image_url, stream=True)
                    for block in response.iter_content(1024):
                        if not block:
                            break
                        handle.write(block)
        return item


class EbayItemPipeline(object):

    def __init__(self):
        print('---------------------EbayItemPipeline init----------------------')

    def process_item(self, item, spider):
        if spider.name not in ['ebay']:
            return item
        print('---------------------EbayItemPipeline ----------------------')
        item_id = self.get_text(item.get('item_id'))
        url = self.get_text(item.get('url'))
        title = BeautifulSoup(self.get_text_title(item.get('title'))).get_text().strip()
        subtitle = self.get_text_title(item.get('subtitle'))
        price = BeautifulSoup(self.get_text_price(item.get('price'))).get_text().strip()
        price_type = self.get_text(item.get('price_type'))
        sold = self.get_text_sold(item.get('sold'))
        watching = self.get_text_watching(item.get('sold'))
        country = self.get_text_country(item.get('country'))
        category = item.get('category')[0]
        # title = item.get('title')
        # subtitle = item.get('subtitle')
        # price = item.get('price')
        # price_type = item.get('price_type')
        # extra = item.get('extra')
        # country = item.get('country')
        print(item_id)
        print(url)
        print(title)
        print(subtitle)
        print(price)
        print(price_type)
        print(sold)
        print(watching)
        print(country)
        print(category)
        print('\n')
        # if sold != 0 or watching != 0:
        if sold != 0:
            # row = [item_id, title, price, sold, watching, country, subtitle, price_type, url]
            # self.csv_file.writerow([unicode(s).encode('utf-8') for s in row])
            item['item_id'] = item_id
            item['url'] = url
            item['title'] = title
            item['subtitle'] = subtitle
            item['price'] = price
            item['price_type'] = price_type
            item['sold'] = sold
            item['watching'] = watching
            item['country'] = country
            item['category'] = category
            try:
                item.save()
            except IntegrityError:
                pass
        return item

    def get_text(self, item):
        if item and len(item) > 0:
            return ' '.join(str(x).strip() for x in item).strip()
        return ''

    def get_text_title(self, item):
        if item and len(item) > 0:
            if 'New listing' in item[0]:
                return item[1].strip()
            else:
                return item[0].strip()
        return ''

    def get_text_price(self, item):
        price = self.get_text(item)
        if price and 'to' in price:
            price = price[0:price.index('to')-2].strip()
        return price

    def get_text_country(self, item):
        if item and len(item) > 0:
            return item[0].replace('From', '').strip()
        return ''

    def get_text_sold(self, item):
        if item and len(item) > 0:
            text = item[0].strip()
            # if 'sold' in text:
            if 'sold' in text and len(text) > 6:
                return text.replace('+', '').replace('sold', '').strip()
        return 0

    def get_text_watching(self, item):
        if item and len(item) > 0:
            text = ' '.join(str(x).strip() for x in item).strip()
            if 'watching' in text:
                for i in item:
                    if 'watching' in i:
                        return i.replace('+', '').replace('watching', '').strip()
        return 0


class AlibabaItemPipeline(object):

    def __init__(self):
        print('---------------------AlibabaItemPipeline init----------------------')

    def process_item(self, item, spider):
        if spider.name not in ['alibabachina']:
            return item
        print('---------------------AlibabaItemPipeline process_item----------------------')
        url = item.get('url')[0]
        title = self.get_text(item.get('title'))
        price = BeautifulSoup(self.get_text(item.get('price'))).get_text().strip()
        location = item.get('location')[0]
        shipping = BeautifulSoup(self.get_text(item.get('shipping'))).get_text().strip()
        content_url = item.get('content_url')
        if content_url and len(content_url) > 0:
            content_data = self.parse_content(content_url[0])
            content_sel = Selector(text=content_data)
            images = content_sel.xpath('//img/@src').extract()
            content_text = content_sel.xpath('//p/node()').extract()
            content_text = self.get_text_content(content_text)
        print title
        print price
        print location
        print shipping
        print images
        print content_text
        item['url'] = url
        item['title'] = title
        item['price'] = price
        item['location'] = location
        item['shipping'] = shipping
        item['image'] = images
        item['content'] = content_text
        item.save()
        return item

    def parse_content(self, url):
        # print('url: %s' % url)
        response = requests.get(url)
        if response and response.status_code == 200:
            data = response.text[10:-3]
            # print('response: %s' % data)
            return data
        return ''

    def get_text(self, item):
        if item and len(item) > 0:
            return ' '.join(x.strip() for x in item).strip()
        return ''

    def get_text_content(self, item):
        data = ''
        if item:
            for i in item:
                text = BeautifulSoup(i).get_text().strip()
                if text and text != "":
                    data += '%s\n' % text
        return data