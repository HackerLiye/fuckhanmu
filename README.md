# 如何优雅地走汗姆

一个大规模、异步式、自动化走汗姆的工具。

感谢[zyc199847](https://github.com/zyc199847)提供的思路,以及[goolhanrry](https://github.com/goolhanrry),
[S-Ex1t](https://github.com/S-Ex1t)提供的脚本。

本工具仅供学习交流，因使用本工具而造成的一切不良后果由使用者自行承担，与作者无关

## 已经实现的功能

- 输入IMEI后获取姓名，对用户致以温暖的问候
- 异步式运行，进入run()函数后无需等待
- 定时运行，在Django后台设置后可以每天特定时间运行run()函数

## 环境依赖

```
pip install django celery flower
pip install django-celery django-celery-results
pip install requests
apt-get install rabbitmq-server
```
## 运行方式

首先在manage.py同级的文件夹下配置数据库
```
python manage.py makemigrations
python manage.py migrate
```
之后运行django
```
python manage.py runserver
```
再启动RabbitMQ
```
rabbitmq-server
```
运行celery worker，celery beat和flower
```commandline
celery worker -A fuckhanmu_web
celery beat -A fuckhanmu_web
celery flower -A fuckhanmu_web
```
如果都没有报错的话应该就可以了。

## 说明
1. 定时任务需要在django后台添加，需要先
```commandline
python manage.py createsuperuser
```
之后输入用户名密码，再进入/admin目录下登陆就会看到一个叫做周期任务的表，
需要在里面手动添加任务，其中的crontab是定义在crontab表里的，这里只是调用了其中的
id，所以views.py里面的添加定时任务函数
```python
PeriodicTask.objects.create(args=json.dumps([str(IMEI)]),
                            enabled=1,
                            name=request.session.get('ID'),
                            crontab_id=1,#需要修改
                            task='autorun.tasks.run',
                            )
```
里面的crontab_id得改一下，要不然会报错。
## 还没有实现的功能
- 根据性别自动设置跑步距离
- 自定义定时任务的时间
- 停止正在运行的任务