# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http.response import JsonResponse
from joblwj.models import SelectScript
from blueking.component.shortcuts import get_client_by_user
from blueking.component.shortcuts import get_client_by_request

# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt

client = get_client_by_user("admin")

# kwargs = {"fields": ["bk_biz_id","bk_biz_name"]}

# 查询业务
def get_host_info():
    result = client.cc.search_business()
    if result["result"]:
        if result['data']['info']:
            biz_name = []
            biz_id = []
            info = {}
            for i in result['data']['info']:
                biz_name.append(i['bk_biz_name'])
                biz_id.append(i['bk_biz_id'])
                info = dict(zip(biz_id, biz_name))
            return info
    else:
        return JsonResponse({"result": False})


def tasks(request):
    tasks = SelectScript.objects.all()
    # 根据条件查询主机
    for biz_id, biz_name in get_host_info().items():
        kwargs = {"bk_biz_id": 2}
        result = client.cc.search_host(kwargs)
        if result["result"]:
            if result['data']['info']:
                hosts = []
                data, res = {}, {}
                host_innerip = []
                os_name = []
                for host_info in result['data']['info']:
                    hosts.append(host_info['host'])
                for i in hosts:
                    host_innerip.append(i['bk_host_innerip'])
                    os_name.append(i['bk_os_name'])
                    data = dict(zip(host_innerip, os_name))
            return render(request, 'tasks.html', {"tasks": tasks, "info": get_host_info().values(), "data": data.items(), "index": enumerate(data, 1)})
        return JsonResponse({"result": False})


def record(request):
    # 获取管理后台所有任务脚本
    tasks = SelectScript.objects.all()
    # 查询所有用户信息
    result = client.bk_login.get_all_users()
    if result["result"]:
        if result['data']:
            usernames = []
            for i in result['data']:
                usernames.append(i['bk_username'])
            return render(request, 'record.html', {"tasks": tasks, "info": get_host_info().values(), "usernames": usernames})
    else:
        return JsonResponse({"result": False})


