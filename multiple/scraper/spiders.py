# -*- coding: utf-8 -*-

from dynamic_scraper.spiders.django_spider import DjangoSpider
from multiple.models import CodeSite, CodeControl, ControlItem


class CodeControlSpider(DjangoSpider):

    name = 'code_control_spider'

    def __init__(self, *args, **kwargs):
        self._set_ref_object(CodeSite, **kwargs)
        self.scraper = self.ref_object.scraper
        self.scrape_url = self.ref_object.url
        self.scheduler_runtime = self.ref_object.scraper_runtime
        self.scraped_obj_class = CodeControl
        self.scraped_obj_item_class = ControlItem
        super(CodeControlSpider, self).__init__(self, *args, **kwargs)

