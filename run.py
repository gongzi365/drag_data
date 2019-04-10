# _*_ coding: utf8 _*_
from bin.ToutiaoList import toutiao_list, toutiao_detail
from bin.TengxunList import tengxun_list, tengxun_detail

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    maps = {}
    maps[0] = [
        'https://www.toutiao.com/api/pc/feed/?category=news_tech&utm_source=toutiao',
        'https://www.toutiao.com/api/pc/feed/?category=news_finance&utm_source=toutiao',
        'https://www.toutiao.com/api/pc/feed/?category=internet&utm_source=toutiao',
        'https://new.qq.com/ch/tech/',
        'https://new.qq.com/ch/finance/',
        'https://new.qq.com/ch/edu/'
    ]
    maps[1] = [
        'https://www.toutiao.com/api/pc/feed/?category=news_travel&utm_source=toutiao',
        'https://www.toutiao.com/api/pc/feed/?category=news_baby&utm_source=toutiao',
        'https://www.toutiao.com/search_content/?offset=0&format=json&keyword=人工智能&autoload=true&count=40&cur_tab=1&from=search_tab',
        'https://www.toutiao.com/search_content/?offset=0&format=json&keyword=大数据&autoload=true&count=40&cur_tab=1&from=search_tab',
        'https://new.qq.com/ch/house/',
        'https://new.qq.com/ch/visit/'
    ]

    if len(sys.argv) == 2:
        key = int(sys.argv[1])
    else:
        key = 0

    lists = maps[key]
    if len(lists) > 0:
        for url in lists:
            if 'toutiao.com' in url:
                # 获取列表
                links = toutiao_list(url)

                # 解析链接并保存
                toutiao_detail(url, links)
            elif 'qq.com' in url:
                # 获取列表
                links = tengxun_list(url)

                # 解析链接并保存
                tengxun_detail(url, links)






