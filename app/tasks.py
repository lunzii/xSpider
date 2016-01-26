# -*- coding: utf-8 -*-

from celery import task
from celery import shared_task
from app.models import LagouCompany
from app.models import WxGzhAccount
from spiders.lagou import SpiderCompany
from spiders.lagou import SpiderJob
from spiders.sogou import SpiderArticle


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
        spider.crawl(_id=item.id, company_id=item.company_id, save=True)
    spider.close()


@task
def crawl_wx_gzh_article():
    items = WxGzhAccount.objects.all()
    for item in items:
        spider = SpiderArticle()
        spider.crawl(wechat_id=item.wechat_id, save=True)
        spider.close()
