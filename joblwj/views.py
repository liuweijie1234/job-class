# -*- coding: utf-8 -*-
import json, base64, datetime, time, copy
from datetime import datetime
from joblwj.celery_tasks import async_status
from celery.task import task
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
                "name": host_info['host']['bk_host_name'],
                "cloud_id": host_info['host']["bk_cloud_id"][0]["id"]
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
        script_id = request.POST.get('script_id')
        obj = SelectScript.objects.get(id=script_id)
        objtest = base64.b64encode(obj.scriptcontent.encode('utf-8'))
        ip_id = request.POST.getlist('ip_id[]')
        ips = {"bk_cloud_id": 0, "ip": 0}
        ip_info = []
        for i in ip_id:
            ips['ip'] = i
            ip_info.append(copy.deepcopy(ips))
        kwargs = {"bk_biz_id": biz_id,
                  "script_content": str(objtest, 'utf-8'),
                  "account": "root",
                  "script_type": 1,
                  "ip_list": ip_info}
        execute_data = client.job.fast_execute_script(kwargs)
        data = execute_data['data']
        result = True
        message = "update success"

        # job_id = data['job_instance_id']
        # kwargs2 = {"bk_biz_id": biz_id,
        #            'job_instance_id': job_id}
        async_status.apply_async(args=[client, data, biz_id, obj, ip_id], kwargs={})
        # job_data = async_status.apply_async(args=[client], kwargs=kwargs2)
        # # job_data = client.job.get_job_instance_status(kwargs2)
        # job_instance = job_data['data']['job_instance']
        # is_finished = job_data['data']['is_finished']
        # status = job_instance['status']
        # create_time = job_instance['create_time'][:-6]
        # start_time = job_instance['start_time'][:-6]
        # if job_instance.get('end_time', ''):
        #     end_time = job_instance['end_time'][:-6]
        # else:
        #     end_time = datetime.datetime.now()
        #
        # Doinfo.objects.create(
        #     businessname=biz_id,
        #     username='admin',
        #     scriptname=obj,
        #     scriptcontent=obj.scriptcontent,
        #     createtime=create_time,
        #     starttime=start_time,
        #     endtime=end_time,
        #     ipcount=len(ip_id),
        #     details=is_finished,
        #     jobid=job_id,
        #     status=status
        # )
    except Exception as err:
        data = []
        result = False
        message = str(err)
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
    data = {"info": get_biz_info().items(),
            "usernames": usernames,
            "tasks": tasks,
            "doinfos": doinfos}
    return render(request, 'record.html', data)


def inquiry(request):
    # 根据前端返回的数据进行查询
    try:
        biz_id = request.POST.get('biz_id')
        username = request.POST.get('username')
        script_id = request.POST.get('script_id')
        time = request.POST.get('time')  #"2020/03/27 - 2020/03/27"
        doinfo = Doinfo.objects.all()
        doinfo = doinfo.filter(businessname=int(biz_id)).filter(username=username).filter(script_id=int(script_id))
        starttime, endtime = time.split('-')
        starttime = starttime.strip().replace('/', '-') + ' 00:00:00'
        endtime = endtime.strip().replace('/', '-') + ' 23:59:00'
        start_time = datetime.strptime(starttime, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(endtime, '%Y-%m-%d %H:%M:%S')
        doinfo = doinfo.filter(starttime__range=(start_time, end_time))
        data = [info.to_dict() for info in doinfo]
        # print(data)
        result = True
        message = "success"
    except Exception as err:
        data = []
        result = False
        message = str(err)
    return JsonResponse({"result": result, "message": message, "data": data})


def statistics(request):
    doinfos = Doinfo.objects.all()
    data = []
    return render(request, 'statistics.html')


def test(request):
    return JsonResponse({"result": True, "message": "hello", "data": "world"})