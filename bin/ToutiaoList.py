# _*_ coding: utf-8 _*_
from utils.Helper import *
from sites.Toutiao import Toutiao
from service.ImportService import ImportService

import json
import time

# 头条链接解析
def toutiao_list(url=''):
    data = []

    if check_file(url):
        html = read_file(url, ext='.list')
    else:
        html = get_url_html(url)
        write_file(url, html, ext='.list')

    # 获取文章url
    resu = json.loads(html)
    if 'data' in resu:
        for vo in resu['data']:
            if "http" not in vo['source_url']:
                dt = {
                    'link': 'https://www.toutiao.com' + vo['source_url'],
                    'image': vo['image_url']
                }
                data.append(dt)

    return data

def toutiao_detail(url, links):
    print json.dumps(links)
    if len(links) > 0:
        for vo in links:
            # todo 检查链接
            if ImportService.check_url(vo['link']):
                continue

            # 延时抓取
            time.sleep(5)

            page = Toutiao(vo['link'])
            data = page.get_content()
            if vo['image'] != '':
                data['image'] = vo['image']
            print json.dumps(data)

            if data['send_time'] == '' or data['title'] == '':
                continue

            # todo 保存数据
            ImportService.insert_handle(data)
            break

            # 删除文件
            #delete_file(vo['link'])


        # 删除列表
        #delete_file(url, ext='.list')


if __name__ == '__main__':
    url = 'https://www.toutiao.com/api/pc/feed/?category=news_tech&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A1E51BA9F727820&cp=5B971788C2A03E1&_signature=jaDHLQAA1kTal492w3Aef42gxz'
    list = toutiao_list(url)

    # 打印解析数据
    print json.dumps(list)

    if len(list) > 0:
        for vo in list:
            page = Toutiao(vo['link'])
            data = page.get_content()
            if vo['image'] != '':
                data['image'] = vo['image']

            # 打印解析数据
            print json.dumps(data)

            break






