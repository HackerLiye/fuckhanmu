# -*- coding: utf-8 -*-

import requests
import datetime
import time
import random
import json
import hashlib

alphabet = list('abcdefghijklmnopqrstuvwxyz')
table = ''.join(alphabet)[:10]


def MD5(s):
    return hashlib.md5(s.encode()).hexdigest()


def encrypt(s):
    result = ''
    for i in s:
        result += table[ord(i) - ord('0')]
    return result


def get_info(IMEI):
    # Generate table Randomly
    random.shuffle(alphabet)

    API_ROOT = 'http://client3.aipao.me/api'
    Version = '2.11'

    # Login
    TokenRes = requests.get(
        API_ROOT + '/%7Btoken%7D/QM_Users/Login_AndroidSchool?IMEICode=' + IMEI)
    TokenJson = json.loads(TokenRes.content.decode('utf8', 'ignore'))
    token = TokenJson['Data']['Token']
    userId = str(TokenJson['Data']['UserId'])
    timespan = str(time.time()).replace('.', '')[:13]
    auth = 'B' + MD5(MD5(IMEI)) + ':;' + token
    nonce = str(random.randint(100000, 10000000))
    sign = MD5(token + nonce + timespan + userId).upper()

    header = {'nonce': nonce, 'timespan': timespan,
              'sign': sign, 'version': Version, 'Accept': None, 'User-Agent': None, 'Accept-Encoding': None,
              'Connection': 'Keep-Alive'}

    # User Information
    InfoRes = requests.get(
        API_ROOT + '/' + token + '/QM_Users/GS')
    InfoJson = json.loads(InfoRes.content.decode('utf8', 'ignore'))
    info = {"NickName": InfoJson['Data']['User']['NickName'],
            "UserID": InfoJson['Data']['User']['UserID'],
            "Sex": InfoJson['Data']['SchoolRun']['Sex']}
    return info


def get_task():
    FLOWER_ROOT = 'http://localhost:5555/'
    successed = requests.get(FLOWER_ROOT + "api/tasks?state=SUCCESS")
    successed = json.loads(successed.content.decode('utf8', 'ignore'))
    # print len(successed)
    failed = requests.get(FLOWER_ROOT + "api/tasks?state=FAILED")
    failed = json.loads(failed.content.decode('utf8', 'ignore'))
    # print len(failed)
    started = requests.get(FLOWER_ROOT + "api/tasks?state=STARTED")
    started = json.loads(started.content.decode('utf8', 'ignore'))
    # print len(started)
    tasks = {"SUCCESS": successed, "FAILED": failed, "STARTED": started}
    return tasks
