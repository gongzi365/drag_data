# _*_ coding: utf-8 _*_
from utils.Helper import *
from sites.Tengxun import Tengxun
from model.ArticleModel import ArticleModel

import json
import time
import re


# 链接解析
def tengxun_list(url=''):
    data = []

    if check_file(url):
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

    return data

def tengxun_detail(url, links):
    print json.dumps(links)

    cate = []
    if 'tech' in url:
        cate = ['科技']


    if len(links) > 0:
        for vo in links:
            # todo 检查链接
            if ArticleModel.check(vo['link']):
                continue

            # 延时抓取
            time.sleep(5)

            page = Tengxun(vo['link'])
            # 补全数据
            page.set_category(cate)
            data = page.get_content()
            if vo['image'] != '':
                data['image'] = vo['image']
            print json.dumps(data)

            if data['send_time'] == '' or data['title'] == '':
                continue

            # todo 保存数据
            ArticleModel.insert(data)

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






