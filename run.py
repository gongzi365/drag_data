# _*_ coding: utf8 _*_
from bin.ToutiaoList import toutiao_list, toutiao_detail
from bin.TengxunList import tengxun_list, tengxun_detail

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':

    lists = [
        # 'https://www.toutiao.com/api/pc/feed/?category=news_tech&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A1E51BA9F727820&cp=5B971788C2A03E1&_signature=jaDHLQAA1kTal492w3Aef42gxz',
        # 'https://www.toutiao.com/api/pc/feed/?category=news_finance&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A1651B997898B9C&cp=5B98E8CBA98CCE1&_signature=sln77gAA6c.lbrO1ZiuOH7JZ-.',
        # 'https://www.toutiao.com/api/pc/feed/?category=internet&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A1657BEB8C89B98&cp=5BBC097B39689E1&_signature=oGRJ9AAA--cvp-2FKUzpVaBkSe',
        # 'https://www.toutiao.com/api/pc/feed/?category=news_travel&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A1153B9B0CB9C76&cp=5BBC89EC17968E1&_signature=pwoaRAAA.MUoyb41bASIJacKGl',
        # 'https://www.toutiao.com/api/pc/feed/?category=news_baby&utm_source=toutiao&widen=1&max_behot_time=1539087566&max_behot_time_tmp=1539087566&tadrequire=true&as=A1359B7BBCB9CF3&cp=5BBC399C0FA33E1&_signature=po3IcAAA.UApTmwBYtU7DaaNyG',
        # 'https://www.toutiao.com/search_content/?offset=0&format=json&keyword=人工智能&autoload=true&count=40&cur_tab=1&from=search_tab',
        # 'https://www.toutiao.com/search_content/?offset=0&format=json&keyword=大数据&autoload=true&count=40&cur_tab=1&from=search_tab',
        # 'https://new.qq.com/ch/tech/',
        # 'https://new.qq.com/ch/finance/',
        # 'https://new.qq.com/ch/edu/',
        # 'https://new.qq.com/ch/house/',
        # 'https://new.qq.com/ch/visit/'

    ]

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






