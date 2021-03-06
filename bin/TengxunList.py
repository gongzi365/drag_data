# _*_ coding: utf-8 _*_
from utils.Helper import *
from sites.Tengxun import Tengxun
from service.ImportService import ImportService
from service import service_logger

import json
import time
import re
import random
import traceback

# 链接解析
def tengxun_list(url=''):
    data = []

    if check_file(url, ext='.list'):
        html = read_file(url, ext='.list')
    else:
        html = get_url_html(url)
        html = unicode(html, 'GBK').encode('UTF-8')
        write_file(url, html, ext='.list')

    res = re.findall('window.chData={(.*?)};', html, re.S)
    if len(res) > 0:
        str = '{' + res[0] + '}'
        arrs = json.loads(str)
        for vo in arrs['data']:
            dt = {
                'link': vo['url'],
                'image': vo['img']
            }
            data.append(dt)
    # 记录日志
    service_logger.warn(data=data)
    return data

def tengxun_detail(url, links):
    print json.dumps(links)

    cate = []
    if 'tech' in url:
        cate = ['科技']
    elif 'finance' in url:
        cate = ['财经']
    elif 'edu' in url:
        cate = ['教育']
    elif 'house' in url:
        cate = ['房产']
    elif 'visit' in url:
        cate = ['旅游']
    elif 'internet' in url or 'tcctit' in url or 'ai' in url:
        cate = ["互联网"]

    if len(links) > 0:
        for vo in links:
            # todo 检查链接
            if ImportService.check_url(vo['link']):
                continue

            # 延时抓取
            tm = random.randint(4, 10)
            time.sleep(tm)

            try:
                page = Tengxun(vo['link'])
                # 补全数据
                page.set_category(cate)
                data = page.get_content()
                if vo['image'] != '':
                    data['image'] = vo['image']
                # 如果图示：开头要加http
                if data['image'] != '' and data['image'][0:2] == '//':
                    data['image'] = 'http:' + data['image']

                # 记录日志
                service_logger.warn(data=data)
                if data['send_time'] == '' or data['title'] == '':
                    continue

                # todo 保存数据
                ImportService.insert_handle(data)
                # break
            except Exception, err:
                service_logger.error("tengxun-exception", {"msg": traceback.format_exc(), "link": vo['link']})

            # 删除文件
            delete_file(vo['link'])

        # 删除列表
        delete_file(url, ext='.list')

if __name__ == '__main__':
    url = 'https://new.qq.com/ch/tech/'
    list = tengxun_list(url)

    # 打印解析数据
    print json.dumps(list)

    if len(list) > 0:
        for vo in list:
            page = Tengxun(vo['link'])
            # 补全数据
            page.set_category(['科技'])

            data = page.get_content()
            if vo['image'] != '':
                data['image'] = vo['image']

            # 打印解析数据
            print json.dumps(data)

            break






