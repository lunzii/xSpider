# -*- coding: utf-8 -*-

from single.models import LagouCompany
from single.models import WxGzhAccount
from celery import task

from single.scraper.lagou import SpiderCompany
from single.scraper.lagou import SpiderJob
from single.scraper.sogou import SpiderArticle


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
