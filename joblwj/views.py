# -*- coding: utf-8 -*-
from django.shortcuts import render


# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt
def tasks(request):

    return render(request, 'tasks.html')


def record(request):

    return render(request, 'record.html')



