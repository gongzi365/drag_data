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

def lottery(accountId, issue, codes):
    codes = codes.replace(',', '&') + '|||||||||'
    post = {
        "accountId": accountId,
        "clientTime": int(time.time())*1000,
        "gameId": "TFPK10",
        "issue": issue,
        "item": [
            {"methodid":"BSC004001001","nums":6,"rebate":"0.00","times":1,"money":0.12,"mode":4,"issueNo":issue,"codes":codes,"playId":[]}
        ]
    }
    url = 'https://df064.com/tools/_ajax/TFPK10/betSingle'
    resp = http_request(url, post)
    print resp

def http_request(url, data):
    headers = {
        'Host': 'df064.com',
        'Content-Type': 'application/json',
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
        "Referer": url,
        "Cookie": "JSESSIONID=0EEB15C3525392D5A52DB66CDF28FACA"
    }
    response = requests.post(url, data=json.dumps(data), headers=headers, timeout=25)
    return response.content

if __name__ == '__main__':

    # https://df064.com/login
    username = 'gongzi'
    userpwd = 'b15013fa3876115daaf8196520d6b0e3'

    # 登录
    login(username, userpwd)

    # # 下单 550270690
    # accountId = 550270690
    # issue = "20181204252"
    # codes = "02,03,04,07,08,09"
    #
    # lottery(accountId=accountId, issue=issue, codes=codes)
