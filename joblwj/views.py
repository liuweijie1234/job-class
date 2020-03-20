# -*- coding: utf-8 -*-
import json, base64
from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponse
from joblwj.models import SelectScript, Doinfo
from blueking.component.shortcuts import get_client_by_user
from blueking.component.shortcuts import get_client_by_request
from blueapps.patch.settings_open_saas import SITE_URL
# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt

client = get_client_by_user("admin")


# 查询业务
def get_biz_info():
    result = client.cc.search_business()
    if result['data']['info']:
        biz_name = []
        biz_id = []
        info = {}
        for i in result['data']['info']:
            biz_name.append(i['bk_biz_name'])
            biz_id.append(i['bk_biz_id'])
            info = dict(zip(biz_name, biz_id))
        return info


# 根据条件查询主机
def ser_host(biz_id):
    kwargs = {"bk_biz_id": biz_id}
    result = client.cc.search_host(kwargs)
    hosts = []
    if result['data']['info']:
        for host_info in result['data']['info']:
            hosts.append({
                "ip": host_info['host']['bk_host_innerip'],
                "os": host_info['host']["bk_os_name"],
                "host_id": host_info['host']["bk_host_id"],
                "cloud_id": host_info['host']["bk_cloud_id"]
            })
    return hosts


# ajax 请求业务相应的host,并返回
def get_host(request):
    try:
        biz_id = request.POST.get('biz_id')
        data = ser_host(biz_id)
        result = True
        message = "update success"
    except Exception as err:
        result = False
        message = str(err)
        data = []
    return JsonResponse({"result": result, "message": message, "data": data})


# 执行任务
def execute_script(request):
    try:
        biz_id = request.POST.get('biz_id')
        scriptcontent = request.POST.get('task.scriptname')
        ip = request.POST.get('ip')
        kwargs = {"bk_biz_id": biz_id,
                  "script_content": 'IyEvYmluL2Jhc2gNCg0KbHMgLWE=',
                  "account": "root",
                  "script_type": 1,
                  "ip_list": [
                      {
                          "bk_cloud_id": 0,
                          "ip": ip
                      }
                  ]}
        data = client.job.fast_execute_script(kwargs)
        result = True
        message = "update success"
    except Exception as err:
        result = False
        message = str(err)
        data = []
    return JsonResponse({"result": result, "message": message, "data": data})


def tasks(request):
    tasks = SelectScript.objects.all()
    data = {"tasks": tasks,
            "info": get_biz_info().items(),
            "data": ser_host(2)}
    return render(request, 'tasks.html', data)


def record(request):
    tasks = SelectScript.objects.all()
    doinfos = Doinfo.objects.all()
    # 查询所有用户信息
    result = client.bk_login.get_all_users()
    if result['data']:
        usernames = []
        for i in result['data']:
            usernames.append(i['bk_username'])
    data = {"tasks": tasks,
            "doinfos": doinfos,
            "info": get_biz_info().items(),
            "usernames": usernames}
    return render(request, 'record.html', data)



