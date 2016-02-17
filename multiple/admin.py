# -*- coding: utf-8 -*-
from django.contrib import admin
from multiple.models import CodeSite, CodeControl


class CodeSiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'url']
    fields = []

admin.site.register(CodeSite, CodeSiteAdmin)


class CodeControlAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'code_site']
    fields = []

admin.site.register(CodeControl, CodeControlAdmin)

