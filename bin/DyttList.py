# _*_ coding: utf-8 _*_
from utils.Helper import *
from sites.Dytt import Dytt
from service.ImportService import ImportService
from pyquery import PyQuery as pq

import json
import time
import re
import sys
import random

reload(sys)
sys.setdefaultencoding('utf-8')


# 链接解析
def dytt_list(url=''):
    data = []

    if check_file(url, ext='.list'):
        html = read_file(url, ext='.list')
    else:
        html = get_url_html(url)
        write_file(url, html, ext='.list')

    doc = pq(html)
    tables = doc('.co_content8 table').items()
    for tb in tables:
        txt = pq(tb)
        links = txt('.ulink').items()
        i = 0
        item = {}
        for link in links:
            i = i+1
            if i == 1:
                cate = pq(link).text()
                cate = cate.replace('[', '').replace(']', '')
                item['cate'] = cate
            else:
                item['title'] = pq(link).text()
                item['link'] = 'http://www.ygdy8.net'+pq(link).attr('href')
        data.append(item)

    return data

def dytt_detail(url, links):
    print json.dumps(links)

    cate = []

    if len(links) > 0:
        for vo in links:
            # todo 检查链接
            if ImportService.check_url(vo['link']):
                continue

            # 延时抓取
            time.sleep(5)

            cate.append(vo['cate'])
            page = Dytt(vo['link'])
            # 补全数据
            page.set_category(cate)
            data = page.get_content(flag=False)
            print json.dumps(data)
            if data['send_time'] == '' or data['title'] == '':
                continue

            # todo 保存数据
            ImportService.insert_handle(data, 'video')
            # break

            # 删除文件
            delete_file(vo['link'])

        # 删除列表
        delete_file(url, ext='.list')

if __name__ == '__main__':
    i = 1
    # total = 203
    total = 2
    while i<total:
        i = i+1
        url = 'http://www.ygdy8.net/html/gndy/china/index.html'
        # url = 'http://www.ygdy8.net/html/gndy/oumei/index.html'
        # url = 'http://www.ygdy8.net/html/gndy/oumei/list_7_%s.html' % (i, )
        print url
        list = dytt_list(url)
        tm = random.randint(5, 10)
        time.sleep(tm)

        # 打印解析数据
        print json.dumps(list)

        if len(list) > 0:
            for vo in list:
                dytt_detail(url, [{"cate": vo['cate'], "link": vo['link']}])
                # break










