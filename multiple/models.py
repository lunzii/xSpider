# -*- coding: utf-8 -*-

from django.db import models
from dynamic_scraper.models import Scraper, SchedulerRuntime
from scrapy_djangoitem import DjangoItem


class CodeSite(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    scraper = models.ForeignKey(Scraper, blank=True, null=True, on_delete=models.SET_NULL)
    scraper_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'scraper_multiple_code_site'
        verbose_name = u'代码网站'


class CodeControl(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    url = models.URLField()
    code_site = models.ForeignKey(CodeSite)
    checker_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'scraper_multiple_code_control'
        verbose_name = u'代码控件'


class ControlItem(DjangoItem):
    django_model = CodeControl
