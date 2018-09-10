# _*_ coding: utf8 _*_
from site.Toutiao import Toutiao

import json

if __name__ == '__main__':

    # 开始抓取
    page = Toutiao("https://www.toutiao.com/a6598090928798302724/")

    data = page.get_content()

    print json.dumps(data)



