# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import requests
from xspider import settings


class XspiderPipeline(object):
    def process_item(self, item, spider):
        print('---------------------process item ----------------------')
        return item


class ImageDownloadPipeline(object):
    def process_item(self, item, spider):
        print('---------------------process item ----------------------')
        if 'image_urls' in item:
            dir_path = '%s/%s' % (settings.IMAGES_STORE, spider.name)

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
