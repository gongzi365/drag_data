# _*_ coding: utf-8 _*_
from utils.Helper import *
from sites.Toutiao import Toutiao

import json
import time

# 头条链接解析
def toutiao_list(links=[]):
    data = []
    if len(links) > 0:
        for url in links:
            if check_file(url):
                html = read_file(url, ext='.list')
            else:
                html = get_url_html(url)
                write_file(url, html, ext='.list')

            # 获取文章url
            resu = json.loads(html)
            if 'data' in resu:
                for vo in resu['data']:
                    dt = {
                        'link': 'https://www.toutiao.com'+vo['source_url'],
                        'image': vo['image_url']
                    }
                    data.append(dt)

    return data

# 插入数据库
def save_data(data):

    return True


if __name__ == '__main__':
    list = toutiao_list(['https://www.toutiao.com/api/pc/feed/?category=news_tech&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A1E51BA9F727820&cp=5B971788C2A03E1&_signature=jaDHLQAA1kTal492w3Aef42gxz'])

    if len(list) > 0:
        for vo in list:
            # todo 查数据库检查连接是否存在
            time.sleep(5)

            page = Toutiao(vo['link'])
            data = page.get_content()
            if vo['image'] != '':
                data['image'] = vo['image']

            # 打印解析数据
            print json.dumps(data)

            # 保存数据
            save_data(data)

            break






