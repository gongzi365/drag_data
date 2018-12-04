# _*_ coding: utf8 _*_

import sys
import time
import requests
import json

reload(sys)
sys.setdefaultencoding('utf-8')

def login(username, userpwd):
    post = {
        "isdefaultLogin": True,
        "loginName": username,
        "loginPwd": userpwd,
        "validCode": "",
        "validateDate": int(time.time())*1000
    }
    url = 'https://df064.com/tools/_ajax/login'
    resp = http_request(url, post)
    print resp

def http_request(url, data):
    headers = {
        'Host': 'df064.com',
        'Content-Type': 'application/json',
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
        "Referer": "https://df064.com/login",
    }
    response = requests.post(url, data=json.dumps(data), headers=headers, timeout=25)
    return response.content

if __name__ == '__main__':

    # https://df064.com/login
    username = 'gongzi'
    userpwd = 'b15013fa3876115daaf8196520d6b0e3'

    # 登录
    login(username, userpwd)
