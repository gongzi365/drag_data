# _*_ coding: utf8 _*_
from bin.ArticleList import toutiao_list, toutiao_detail

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


if __name__ == '__main__':

    lists = [
        'https://www.toutiao.com/api/pc/feed/?category=news_tech&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A1E51BA9F727820&cp=5B971788C2A03E1&_signature=jaDHLQAA1kTal492w3Aef42gxz'
    ]

    if len(lists) > 0:
        for url in lists:
            if 'toutiao' in url:
                # 获取列表
                links = toutiao_list(url)

                # 解析链接并保存
                toutiao_detail(url, links)






