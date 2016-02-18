# -*- coding: utf-8 -*-
from celery import task
from django.db.models import Q
from dynamic_scraper.utils.task_utils import TaskUtils
from multiple.models import CodeSite, CodeControl


@task()
def crawl_cocoa_controls():
    t = TaskUtils()
    kwargs = {}
    args = (Q(name='CocoaControls-iOS'),)
    t.run_spiders(CodeSite, 'scraper', 'scraper_runtime', 'code_control_spider', *args, **kwargs)


@task()
def crawl_code_for_app():
    t = TaskUtils()
    kwargs = {}
    args = (Q(name='Code4App'),)
    t.run_spiders(CodeSite, 'scraper', 'scraper_runtime', 'code_control_spider', *args, **kwargs)
