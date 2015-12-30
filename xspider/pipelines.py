# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import re
import requests
from bs4 import BeautifulSoup
from django.db import IntegrityError
from scrapy.selector import Selector
import leancloud
from xspider import settings


leancloud.init('8PLBPnjECEjhBzGmMy9erk6L-gzGzoHsz', 'vl5PdecpWBaC3IYtgBrSAoAl')
Gallery = leancloud.Object.extend('Gallery')
Photo = leancloud.Object.extend('Photo')


class ImageDownloadPipeline(object):
    def process_item(self, item, spider):
        if spider.name not in ['meizitu']:
            return item
        print('---------------------ImageDownloadPipeline ----------------------')
        print(item)
        # 去重
        query = leancloud.Query(Gallery)
        query.equal_to('url', item['url'][0])
        urls = query.find()
        if len(urls) > 0:
            pass
        else:
            gallery = Gallery()
            gallery.set('title', item['title'][0])
            gallery.set('url', item['url'][0])
            gallery.set('cover', item['image_urls'][0])
            gallery.set('tag', item['tags'][0])
            gallery.set('day', item['day'][0])
            gallery.set('year', item['month_year'][0])
            gallery.save()
            for image in item['image_urls']:
                photo = Photo()
                photo.set('gallery', gallery)
                photo.set('image', image)
                photo.save()
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
        item_id = self.get_text(item.get('item_id'))
        title = self.get_text(item.get('title'))
        url = 'http://detail.1688.com/offer/%s.html' % item_id
        company_id = self.get_text(item.get('company_id'))
        company_name = self.get_text(item.get('company_name'))
        company_url = self.get_text(item.get('company_url'))
        company_location = self.get_text(item.get('company_location'))
        sold_item = self.get_text_sold(item.get('sold_item'))
        sold_person = self.get_text(item.get('sold_person'))
        price = self.get_text(item.get('price'))
        category = item.get('category')[0]
        print(item_id)
        print(title)
        print(url)
        print(company_id)
        print(company_name)
        print(company_url)
        print(company_location)
        print(price)
        print(sold_item)
        print(sold_person)
        print(category)
        print('------------')
        item['item_id'] = item_id
        item['title'] = title
        item['url'] = url
        item['company_id'] = company_id
        item['company_name'] = company_name
        item['company_url'] = company_url
        item['company_location'] = company_location
        item['price'] = price
        item['sold_item'] = sold_item
        item['sold_person'] = sold_person
        item['category'] = category
        item.save()
        return item

    def get_text(self, item):
        if item and len(item) > 0:
            return ' '.join(x.strip() for x in item).strip()
        return ''

    def get_text_sold(self, item):
        price = self.get_text(item)
        if u'万' in price:
            price = price.replace(u'万', '')
            price = int(float(price) * 10000)
        return price


class AliexpressItemPipeline(object):

    def __init__(self):
        print('---------------------AliexpressItemPipeline init----------------------')

    def process_item(self, item, spider):
        print('spider: %s' % spider.name)
        if spider.name not in ['aliexpress']:
            return item
        print('---------------------AliexpressItemPipeline process_item----------------------')
        item_id = self.get_text(item.get('item_id'))
        url = self.get_text(item.get('url'))
        title = self.get_text(item.get('title'))
        price = self.get_text(item.get('price'))
        unit = self.get_text(item.get('unit'))
        min_order = self.get_text(item.get('min_order'))
        shipping = self.get_text(item.get('shipping'))
        rate_num = self.get_text_num(item.get('rate_num'))
        order_num = self.get_text_num(item.get('order_num'))
        store_name = self.get_text(item.get('store_name'))
        store_url = self.get_text(item.get('store_url'))
        category = item.get('category')[0]
        print(item_id)
        print(url)
        print(title)
        print(price)
        print(unit)
        print(min_order)
        print(shipping)
        print(rate_num)
        print(order_num)
        print(store_name)
        print(store_url)
        print(category)
        print('------------')
        item['item_id'] = item_id
        item['title'] = title
        item['url'] = url
        item['price'] = price
        item['unit'] = unit
        item['min_order'] = min_order
        item['shipping'] = shipping
        item['rate_num'] = rate_num
        item['order_num'] = order_num
        item['store_name'] = store_name
        item['store_url'] = store_url
        item['category'] = category
        item.save()
        return item

    def get_text(self, item):
        if item and len(item) > 0:
            return ' '.join(x.strip() for x in item).strip()
        return ''

    def get_text_num(self, item):
        item = re.findall(r'\d+', self.get_text(item))
        if item and len(item) > 0:
            return item[0]
        return 0
