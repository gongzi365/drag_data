# _*_ coding: utf8 _*_
from bin.DyttList import dytt_list, dytt_detail
from service.ImportService import ImportService

import sys
import time
import random

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    i = 5
    total = 209
    # total = 9
    while i < total:
        i = i + 1
        # 日韩电影 url = 'http://www.ygdy8.net/html/gndy/rihan/index.html'
        # 欧美电影 url = 'http://www.ygdy8.net/html/gndy/oumei/index.html'
        # 国内电影 url = 'http://www.ygdy8.net/html/gndy/china/index.html'
        # 综合电影 url = 'http://www.ygdy8.net/html/gndy/jddy/index.html'
        # 最新电影 url = 'http://www.ygdy8.net/html/gndy/dyzz/index.html'
        # url = 'http://www.ygdy8.net/html/gndy/oumei/list_7_%s.html' % (i, )
        # url = 'http://www.ygdy8.net/html/gndy/china/list_4_%s.html' % (i, )
        # url = 'http://www.ygdy8.net/html/gndy/rihan/list_6_%s.html' % (i, )
        url = 'http://www.ygdy8.net/html/gndy/jddy/list_63_%s.html' % (i, )
        # url = 'http://www.ygdy8.net/html/gndy/dyzz/list_23_%s.html' % (i, )
        print url

        list = dytt_list(url)
        tm = random.randint(10, 15)
        time.sleep(tm)
        # list = [{"link": "http://www.ygdy8.net/html/gndy/jddy/20140429/45014.html"}]

        # 抓取页面数据
        dytt_detail(url, list)
        # if len(list) > 0:
        #     for vo in list:
        #         dytt_detail(url, [vo])
        #         break

        # 停止
        # break