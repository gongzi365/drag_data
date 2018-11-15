# _*_ coding: utf-8 _*_
from Drag import Drag
from pyquery import PyQuery as pq
from utils.Helper import *
import HTMLParser

import re
import json

class Toutiao(Drag):
    platform = '今日头条'
    type = 'toutiao'

    def __int__(self, url):
        self.url = url
        self.html = None
        self.doc = None

        Drag.__init__(self, url)

    # 获取页面
    def _handle(self):
        if check_file(self.url):
            self.html = read_file(self.url)
        else:
            html = get_url_html(self.url)
            html_parser = HTMLParser.HTMLParser()
            self.html = html_parser.unescape(html)
            write_file(self.url, self.html)
        self.cate = []

    def set_category(self, cate):
        self.cate = cate

    # 分类
    def _category(self):
        if len(self.cate) > 0:
            return self.cate

        cate = []
        res = re.findall("chineseTag: '(.*?)'", self.html, re.S)
        # print res
        if len(res) > 0:
            cate.append(res[0])

        return cate

    # 标题
    def _title(self):
        title = ''
        res = re.findall("articleInfo: {.*?}", self.html, re.S)
        # print res
        if len(res) > 0:
            resu = re.search("title: '(.*?)'", res[0], flags=0)
            if resu:
                str = resu.group()
                str = str.replace("'", '')
                title = str.replace("title: ", '')

        return title

    # 内容
    def _content(self):
        content = ''
        res = re.findall("articleInfo: {.*?}", self.html, re.S)
        # print res
        if len(res) > 0:
            resu = re.search("content: '(.*?)'", res[0], flags=0)
            if resu:
                str = resu.group()
                str = str.replace("'", '')
                content = str.replace("content: ", '')

        return content

    # 标签
    def _tags(self):
        tags = []
        res = re.findall(" tags: \[(.*?)\]", self.html, re.S)
        # print res
        if len(res) > 0:
            str = '['+res[0]+']'
            arrs = json.loads(str)
            for vo in arrs:
                tags.append(vo['name'])

        return ','.join(tags)

    # 图片
    def _image(self):
        image = ''
        imgs = re.findall('<img src="(.*?)"', self.html, re.S)
        if len(imgs) > 0:
            image = imgs[0]

        return image

    # 发布时间
    def _send_time(self):
        send_time = ''
        res = re.findall("time: '(.*?)'", self.html, re.S)
        # print res
        if len(res) > 0:
            send_time = res[0]

        return send_time

    # 其它数据
    def _others(self):

        return []











