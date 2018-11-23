# _*_ coding: utf-8 _*_
from utils.Helper import *
from sites.Toutiao import Toutiao
from service.ImportService import ImportService
from service import service_logger

import json
import time
import random
import traceback

# 头条链接解析
def toutiao_list(url=''):
    data = []

    if check_file(url, ext='.list'):
        html = read_file(url, ext='.list')
    else:
        cookie = 'UM_distinctid=165e23b8bd863a-02b6bf44638b1e-541b371f-100200-165e23b8bd9812; tt_webid=6601789411817768455; WEATHER_CITY=%E5%8C%97%E4%BA%AC; uuid="w:be3b8ee49353488b825ded5ccbcf16b3"; CNZZDATA1259612802=1933104973-1537094542-%7C1539087142; __tasessionId=qgp2gufge1539087164145; csrftoken=afc50bb8fb759393b3c1da8340182cd6; tt_webid=6601789411817768455'
        html = get_url_html(url, cookie)
        write_file(url, html, ext='.list')

    #print html
    # 获取文章url
    resu = json.loads(html)
    if 'data' in resu:
        for vo in resu['data']:
            if 'item_source_url' in vo and 'media_avatar_url' in vo:
                if "http" not in vo['item_source_url'] and 'local//' not in vo['item_source_url']:
                    dt = {
                        'link': 'https://www.toutiao.com' + vo['item_source_url'],
                        'image': vo['media_avatar_url']
                    }
                    data.append(dt)
            elif 'source_url' in vo and 'image_url' in vo:
                if "http" not in vo['source_url'] and 'local//' not in vo['item_source_url']:
                    dt = {
                        'link': 'https://www.toutiao.com' + vo['source_url'],
                        'image': vo['image_url']
                    }
                    data.append(dt)

    return data

def toutiao_detail(url, links):
    print json.dumps(links)

    cate = []
    if 'news_baby' in url:
        cate = ['教育']
    elif 'news_travel' in url:
        cate = ['旅游']
    elif '人工智能' in url or '大数据' in url:
        cate = ['技术']

    if len(links) > 0:
        for vo in links:
            # todo 检查链接
            if ImportService.check_url(vo['link']):
                continue

            # 延时抓取
            tm = random.randint(4, 10)
            time.sleep(tm)

            try:
                page = Toutiao(vo['link'])
                # 补全数据
                if len(cate) > 0:
                    page.set_category(cate)

                data = page.get_content()
                if vo['image'] != '':
                    data['image'] = vo['image']
                # 如果图示：开头要加http
                if data['image'] != '' and data['image'][0:2] == '//':
                    data['image'] = 'http:' + data['image']

                print json.dumps(data)
                if data['send_time'] == '' or data['title'] == '':
                    continue

                # todo 保存数据
                ImportService.insert_handle(data)
                # break
            except Exception, err:
                service_logger.error("toutiao-exception", {"msg": traceback.format_exc(), "link": vo['link']})

            # 删除文件
            delete_file(vo['link'])

        # 删除列表
        delete_file(url, ext='.list')


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






