# _*_ coding: utf-8 _*_
from Drag import Drag
from pyquery import PyQuery as pq
from utils.Helper import *

import re
import json

class Tengxun(Drag):
    platform = '腾讯新闻'
    type = 'tengxun'

    def __int__(self, url):
        self.url = url
        self.html = None
        self.doc = None
        self.cate = []
        self.title = ''
        self.send_time = ''
        self.tags = ''

        Drag.__init__(self, url)

    # 获取页面
    def _handle(self):
        if check_file(self.url):
            self.html = read_file(self.url)
        else:
            html = get_url_html(self.url)
            self.html = unicode(html, 'GBK').encode('UTF-8')
            write_file(self.url, self.html)

        # 转doc对象
        self.doc = pq(self.html)

    def set_category(self, cate):

        self.cate = cate

    # 分类
    def _category(self):
        res = re.findall('window.DATA = {(.*?)}', self.html, re.S)
        if len(res) > 0:
            str = '{' + res[0] + '}'
            arrs = json.loads(str)

            if 'title' in arrs:
                self.title = arrs['title']
            if 'pubtime' in arrs:
                self.send_time = arrs['pubtime']
            if 'tags' in arrs:
                self.tags = arrs['tags']

        return self.cate

    # 标题
    def _title(self):

        return self.title

    # 内容
    def _content(self):
        content = ''

        res = re.findall('<div class="content-article">(.*?)<div id="Status"></div>', self.html, re.S)
        if len(res) > 0:
            content = res[0]

        return content

    # 标签
    def _tags(self):

        return self.tags

    # 图片
    def _image(self):
        image = ''
        imgs = re.findall('<img src="(.*?)"', self.html, re.S)
        if len(imgs) > 0:
            image = imgs[0]

        return image

    # 发布时间
    def _send_time(self):

        return self.send_time











