# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .tasks import run
from django.shortcuts import render
from info import get_info, get_task
from djcelery.models import PeriodicTask
from celery.schedules import crontab
import json
# Create your views here.


def index(request):
    # 获得任务统计信息
    tasks = get_task()
    task_count = {'SUCCESS': len(tasks['SUCCESS']),
                  'FAILED': len(tasks['FAILED']),
                  'STARTED': len(tasks['STARTED'])}

    # 如果已经输入过IMEI
    if request.session.get('IMEI'):
        info = get_info(request.session.get('IMEI'))
        name = info['NickName']
        id = info['UserID']
        request.session['Name'] = name
        request.session['ID'] = id
        message = ""
        message_run = "未进行跑步任务"
        message_schedule = "未添加定时任务"
        # 显示立刻跑步的信息
        for detail in tasks["STARTED"].values():
            # 检测等待队列，如果有则提示
            if detail['args'][3:-3] == request.session.get('IMEI'):
                message_run = "任务已经在队列中"
                # request.session['Applied'] = True

        # 显示定时跑步的信息
        try:
            task = PeriodicTask.objects.get(name=request.session.get('ID'))
            message_schedule = str(task.crontab)
        except:
            pass
        return render(request, 'detail.html', {"NickName": name, "TASKS": task_count,
                                               "MESSAGE": message, "APPLIED": request.session.get('Applied'),
                                               "MESSAGE_RUN": message_run, "MESSAGE_SCHEDULE": message_schedule})

    else:
        # 处理IMEI的POST请求
        if request.method == 'POST':
            request.session['IMEI'] = request.POST['IMEI']
            info = get_info(request.session.get('IMEI'))
            name = info['NickName']
            return render(request, 'detail.html', {"NickName": name, "TASKS": task_count})
        # 第一次访问要求输入IMEI
        return render(request, 'index.html')


def start_run(request):
    tasks = get_task()
    # 检测有没有跑过的标记
    message = ""
    flag = True
    # if not request.session.get('Applied'):
    #     # 如果没有就标记上，然后开始跑步
    #     request.session['Applied'] = True
    #     run.delay(request.session.get('IMEI'))
    #     message = "跑步成功！"
    # else:
    for detail in tasks["STARTED"].values():
        # 如果在队列中检测到对应的任务，就显示已经跑过了
        print detail['args']
        if detail['args'][3:-3] == request.session.get('IMEI'):
            message = "现在正在队列中哦，不要着急"
            flag = False
    if flag:
        run.delay(request.session.get('IMEI'))
        message = "跑步成功！"
    return render(request, 'result.html', {"Message": message})


def schedule(request):
    IMEI = request.session.get('IMEI')
    try:
        PeriodicTask.objects.create(args=json.dumps([str(IMEI)]),
                                    enabled=1,
                                    name=request.session.get('ID'),
                                    crontab_id=3,
                                    task='autorun.tasks.run',
                                    )
        message = '添加成功'
    except:
        message = '无需重复添加'
    task = PeriodicTask.objects.get(name=request.session.get('ID'))
    message += str(task.crontab)
    # print message
    return render(request, 'result.html', {"Message": message})


def test(request):
    pass