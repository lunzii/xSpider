# -*- coding: utf-8 -*-

from django.contrib import admin
from app.models import LagouCompany
from app.models import LagouJob


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

