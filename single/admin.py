# -*- coding: utf-8 -*-

from django.contrib import admin
from single.models import LagouCompany
from single.models import LagouJob
from single.models import WxGzhAccount
from single.models import WxGzhArticle


class LagouCompanyAdmin(admin.ModelAdmin):
    list_display = ['company_id', 'company_name', 'company_type', 'company_step', 'company_city',
                    'interview_count', 'job_count', 'resume_rate']
    fields = []

admin.site.register(LagouCompany, LagouCompanyAdmin)


class LagouJobAdmin(admin.ModelAdmin):
    list_display = ['company_id', 'company_name', 'job_id', 'job_name', 'job_salary',
                    'job_publish_date']
    fields = []

admin.site.register(LagouJob, LagouJobAdmin)


class WxGzhAccountAdmin(admin.ModelAdmin):
    list_display = ['wechat_id', 'wechat_name', 'wechat_type', 'wechat_code']
    fields = []

admin.site.register(WxGzhAccount, WxGzhAccountAdmin)


class WxGzhArticleAdmin(admin.ModelAdmin):
    list_display = ['wechat_id', 'title', 'publish']
    fields = []

admin.site.register(WxGzhArticle, WxGzhArticleAdmin)

