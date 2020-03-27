# -*- coding: utf-8 -*-
from django.contrib import admin
from joblwj.models import SelectScript, Doinfo
# Register your models here.


class Script(admin.ModelAdmin):
    list_display = ['scriptname', 'scriptcontent']
    search_fields = ['scriptname', 'scriptcontent']

class Info(admin.ModelAdmin):
    list_display = ['businessname', 'username', 'scriptname', 'scriptcontent', 'starttime', 'ipcount', 'status']
    search_fields = ['businessname', 'username', 'scriptname']
    date_hierarchy = 'starttime'


admin.site.register(SelectScript, Script)
admin.site.register(Doinfo, Info)