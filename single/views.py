# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from single import tasks


def lagou_company(request):
    tasks.crawl_lagou_company.delay()
    return HttpResponse('succeed')


def lagou_job(request):
    tasks.crawl_lagou_job.delay()
    return HttpResponse('succeed')


def tax_article(request):
    tasks.crawl_tax_article.delay()
    return HttpResponse('succeed')
