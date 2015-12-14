# -*- coding: utf-8 -*-

from celery import task
from celery import shared_task
from app.models import LagouCompany
from spiders.lagou import SpiderCompany
from spiders.lagou import SpiderJob


@task
def crawl_lagou_company():
    spider = SpiderCompany()
    spider.crawl(save=False)
    spider.close()


@task
def crawl_lagou_job():
    spider = SpiderJob()
    items = LagouCompany.objects.all()
    for item in items:
        spider.crawl(company_id=item.company_id, save=False)
    spider.close()

