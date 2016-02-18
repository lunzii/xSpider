# -*- coding: utf-8 -*-
from django.contrib import admin
from multiple.models import CodeSite, CodeControl


class CodeSiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'url_']
    fields = []

    def url_(self, instance):
            return '<a href="{url}" target="_blank">{title}</a>'.format(
                url=instance.url, title=instance.url)
    url_.allow_tags = True
admin.site.register(CodeSite, CodeSiteAdmin)


class CodeControlAdmin(admin.ModelAdmin):
    list_display = ['title', 'source_', 'platform', 'code_site']
    fields = []

    def source_(self, instance):
        return '<a href="{url}" target="_blank">{title}</a>'.format(
            url=instance.source, title=instance.source)
    source_.allow_tags = True

admin.site.register(CodeControl, CodeControlAdmin)

