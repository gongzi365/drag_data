# _*_ coding: utf8 _*_
from bin.DyttList import dytt_list, dytt_detail

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    lists = [
        'http://www.ygdy8.net/html/gndy/rihan/index.html',
        'http://www.ygdy8.net/html/gndy/oumei/index.html',
        'http://www.ygdy8.net/html/gndy/china/index.html',
        'http://www.ygdy8.net/html/gndy/jddy/index.html',
        'http://www.ygdy8.net/html/gndy/dyzz/index.html'
    ]

    if len(lists) > 0:
        for url in lists:
            if 'www.ygdy8.net' in url:
                # 获取列表
                links = dytt_list(url)

                # 解析链接并保存
                dytt_detail(url, links)







