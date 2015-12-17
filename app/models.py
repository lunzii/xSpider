# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import django.utils.timezone as timezone

from django.db import models
import logging
logger = logging.getLogger(__name__)


class LagouCompany(models.Model):
    company_id = models.CharField(max_length=16, null=True)
    company_name = models.CharField(max_length=256, null=True)
    company_desc = models.CharField(max_length=256, null=True)
    company_type = models.CharField(max_length=128, null=True)
    company_step = models.CharField(max_length=128, null=True)
    company_financing = models.CharField(max_length=128, null=True)
    company_city = models.CharField(max_length=128, null=True)
    company_employee = models.CharField(max_length=128, null=True)
    interview_count = models.CharField(max_length=16, null=True)
    job_count = models.CharField(max_length=16, null=True)
    resume_rate = models.CharField(max_length=16, null=True)
    created_id = models.CharField(max_length=128, null=True)
    created_at = models.DateField(default=timezone.now)

    class Meta:
        db_table = 'spider_lagou_company'
        verbose_name = u'拉勾公司'


class LagouJob(models.Model):
    company_id = models.CharField(max_length=16, null=True)
    company_name = models.CharField(max_length=256, null=True)
    job_id = models.CharField(max_length=16, null=True)
    job_salary = models.CharField(max_length=256, null=True)
    job_name = models.CharField(max_length=128, null=True)
    job_desc = models.CharField(max_length=128, null=True)
    job_publish_date = models.CharField(max_length=128, null=True)
    created_id = models.CharField(max_length=128, null=True)
    created_at = models.DateField(default=timezone.now)

    class Meta:
        db_table = 'spider_lagou_job'
        verbose_name = u'拉勾职位'


class TaxAccount(models.Model):
    wechat_id = models.CharField(max_length=128, null=True)
    wechat_name = models.CharField(max_length=128, null=True)
    wechat_type = models.CharField(max_length=128, null=True)
    wechat_code = models.CharField(max_length=512, null=True, blank=True)
    created_at = models.DateField(default=timezone.now)

    class Meta:
        db_table = 'spider_tax_account'
        verbose_name = u'税务订阅号'


class TaxArticle(models.Model):
    wechat_id = models.CharField(max_length=128, null=True)
    title = models.CharField(max_length=256, null=True)
    desc = models.TextField(null=True)
    image = models.URLField(null=True, blank=True)
    publish = models.CharField(max_length=64, null=True)
    link = models.URLField(null=True)
    url = models.URLField(null=True, blank=True)
    created_at = models.DateField(default=timezone.now)

    class Meta:
        db_table = 'spider_tax_article'
        verbose_name = u'税务文章'
