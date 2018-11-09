# _*_ coding: utf8 _*_
from bin.ToutiaoList import toutiao_list, toutiao_detail
from bin.TengxunList import tengxun_list, tengxun_detail

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':

    lists = [
        'https://www.toutiao.com/api/pc/feed/?category=news_tech&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A145BBEE05F739A&cp=5BE59733397A7E1&_signature=jaFCXQAA1lACYuYsAkyR0o2hQk',
        'https://www.toutiao.com/api/pc/feed/?category=news_finance&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A145CB4ED5373C6&cp=5BE577433CE63E1&_signature=jYqQMgAA1nwCSTRD8dL1dI2KkC',
        'https://www.toutiao.com/api/pc/feed/?category=internet&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A1550B3E5507404&cp=5BE527F4E024BE1&_signature=jUiO9AAA1roCiyqF-HPD041Iju',
        'https://www.toutiao.com/api/pc/feed/?category=news_travel&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A115AB1E35F7452&cp=5BE5D70425121E1&_signature=jR4TnQAA1wgC3bfsMTCxy40eE4',
        'https://www.toutiao.com/api/pc/feed/?category=news_baby&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A1152BFE0587474&cp=5BE5A75467647E1&_signature=jPic7gAA1yoDOzifRdzyJ4z4nP',
        'https://www.toutiao.com/search_content/?offset=0&format=json&keyword=人工智能&autoload=true&count=40&cur_tab=1&from=search_tab',
        'https://www.toutiao.com/search_content/?offset=0&format=json&keyword=大数据&autoload=true&count=40&cur_tab=1&from=search_tab',
        'https://new.qq.com/ch/tech/',
        'https://new.qq.com/ch/finance/',
        'https://new.qq.com/ch/edu/',
        'https://new.qq.com/ch/house/',
        'https://new.qq.com/ch/visit/'

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






