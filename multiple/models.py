# -*- coding: utf-8 -*-

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete
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
    url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    thumbnail = models.URLField(blank=True)
    source = models.URLField(blank=True)
    tags = models.CharField(max_length=512, blank=True)
    category = models.CharField(max_length=512, blank=True)
    platform = models.CharField(max_length=16, blank=True)
    code_site = models.ForeignKey(CodeSite)
    checker_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'scraper_multiple_code_control'
        verbose_name = u'代码控件'


class ControlItem(DjangoItem):
    django_model = CodeControl


@receiver(pre_delete)
def pre_delete_handler(sender, instance, using, **kwargs):
    if isinstance(instance, CodeSite):
        if instance.scraper_runtime:
            instance.scraper_runtime.delete()

    if isinstance(instance, CodeControl):
        if instance.checker_runtime:
            instance.checker_runtime.delete()

pre_delete.connect(pre_delete_handler)
