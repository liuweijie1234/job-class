# -*- coding: utf-8 -*-
from django.shortcuts import render
from joblwj.models import SelectScript
from blueking.component.shortcuts import get_client_by_user
from blueking.component.shortcuts import get_client_by_request

# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt
# "bk_app_code": "job-class",
# "bk_app_secret": "ab784530-398f-4a75-819a-4fdf63dfddea",
# "bk_token": "Delqj_TcSBLNmBy0yOTpht7Y_ZXdhsziSLo5Mg0fUbU",
client = get_client_by_user("admin")

# kwargs = {"fields": ["bk_biz_id","bk_biz_name"]}
# 查询业务
result = client.cc.search_business()
a = result['data']['info']
b = []
for i in a:
    b.append(i['bk_biz_name'])

#查询所有用户信息
result1 = client.bk_login.get_all_users()
a1 = result1['data']
b1 = []
for i in a1:
    b1.append(i['bk_username'])

taskses = SelectScript.objects.all()


def tasks(request):

    return render(request, 'tasks.html', {"taskses": taskses, "business": b})


def record(request):

    return render(request, 'record.html', {"taskses": taskses, "business": b, "users":b1})



