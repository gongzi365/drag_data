# _*_ coding: utf8 _*_
from bin.ToutiaoList import toutiao_list, toutiao_detail
from bin.TengxunList import tengxun_list, tengxun_detail

# from wordpress_xmlrpc import Client, WordPressPost
# from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
# from wordpress_xmlrpc.methods.users import GetUserInfo
# from wordpress_xmlrpc.methods import posts
# from wordpress_xmlrpc.methods import taxonomies
# from wordpress_xmlrpc import WordPressTerm
# from wordpress_xmlrpc.compat import xmlrpc_client
# from wordpress_xmlrpc.methods import media, posts

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# wp = Client('http://www.newmedia.me/xmlrpc.php', 'science', 'gongzi7246883')
# print wp
# quit(1111)

if __name__ == '__main__':

    lists = [
        # 'https://www.toutiao.com/api/pc/feed/?category=news_tech&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A1E51BA9F727820&cp=5B971788C2A03E1&_signature=jaDHLQAA1kTal492w3Aef42gxz',
        # 'https://www.toutiao.com/api/pc/feed/?category=news_finance&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A1651B997898B9C&cp=5B98E8CBA98CCE1&_signature=sln77gAA6c.lbrO1ZiuOH7JZ-.',
        'https://new.qq.com/ch/tech/'
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






