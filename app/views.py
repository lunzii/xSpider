# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from app.models import LagouCompany
from spiders.lagou import SpiderCompany
from spiders.lagou import SpiderJob


def lagou_company(request):
    spider = SpiderCompany()
    # spider.crawl()
    spider.close()
    return HttpResponse('succeed')


def lagou_job(request):
    spider = SpiderJob()
    items = LagouCompany.objects.all()
    for item in items:
        spider.crawl(company_id=item.company_id, save=True)
    spider.close()
    return HttpResponse('succeed')
