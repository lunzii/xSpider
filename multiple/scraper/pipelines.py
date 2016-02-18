# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
from bs4 import BeautifulSoup
from django.db import IntegrityError
import leancloud

import logging
from scrapy.exceptions import DropItem
from dynamic_scraper.models import SchedulerRuntime


class CodeControlPipeline(object):

    def process_item(self, item, spider):
        if spider.conf['DO_ACTION']:
            try:
                item['code_site'] = spider.ref_object

                checker_rt = SchedulerRuntime(runtime_type='C')
                checker_rt.save()
                item['checker_runtime'] = checker_rt

                item.save()
                spider.action_successful = True
                spider.log("Item saved.", logging.INFO)

            except IntegrityError, e:
                spider.log(str(e), logging.ERROR)
                spider.log(str(item._errors), logging.ERROR)
                raise DropItem("Missing attribute.")
        else:
            if not item.is_valid():
                spider.log(str(item._errors), logging.ERROR)
                raise DropItem("Missing attribute.")

        return item