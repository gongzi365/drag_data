# _*_ coding: utf-8 _*_
from utils.Helper import *
from sites.Dytt import Dytt
from service.ImportService import ImportService
from pyquery import PyQuery as pq
from service import service_logger

import json
import time
import re
import sys
import random
import traceback

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

    if html == '':
        return data

    doc = pq(html)
    tables = doc('.co_content8 table').items()
    for tb in tables:
        txt = pq(tb)
        links = txt('.ulink').items()
        item = {}
        for link in links:
            href = pq(link).attr('href')
            if 'index.html' not in href:
                item['title'] = pq(link).text()
                item['link'] = 'http://www.ygdy8.net'+pq(link).attr('href')

        data.append(item)

    # 记录日志
    service_logger.warn(data=data)
    return data

def dytt_detail(url, links):
    print json.dumps(links)

    cate = []
    if 'jddy' in url:
        cate = ['综合电影']
    elif 'oumei' in url:
        cate = ['欧美电影']
    elif 'china' in url:
        cate = ['国内电影']
    elif 'rihan' in url:
        cate = ['日韩电影']
    elif 'dyzz' in url:
        cate = ['最新电影']


    if len(links) > 0:
        for vo in links:
            print vo['link']
            # todo 检查链接
            if ImportService.check_url(vo['link']):
                continue

            # 延时抓取
            tm = random.randint(4, 10)
            time.sleep(tm)

            try:
                page = Dytt(vo['link'])
                # 补全数据
                page.set_category(cate)

                data = page.get_content(flag=False)
                # 记录日志
                service_logger.warn(data=data)
                if data['send_time'] == '' or data['title'] == '':
                    continue

                # todo 保存数据
                ImportService.insert_handle(data, 'video')
                # break

            except Exception, err:
                service_logger.error("dytt-exception", {"msg": traceback.format_exc(), "link": vo['link']})

            # 删除文件
            delete_file(vo['link'])

        # 删除列表
        delete_file(url, ext='.list')

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
        url = 'http://www.ygdy8.net/html/gndy/oumei/list_7_%s.html' % (i, )
        # url = 'http://www.ygdy8.net/html/gndy/china/list_4_%s.html' % (i, )
        # url = 'http://www.ygdy8.net/html/gndy/rihan/list_6_%s.html' % (i, )
        # url = 'http://www.ygdy8.net/html/gndy/jddy/list_63_%s.html' % (i, )
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








