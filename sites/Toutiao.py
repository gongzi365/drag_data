# _*_ coding: utf-8 _*_
from service import service_logger
from Drag import Drag
from config.Config import Config
from pyquery import PyQuery as pq

import hashlib
import os
import requests
import re
import json

class Toutiao(Drag):
    platform = '今日头条'
    type = 'toutiao'

    def __int__(self, url):
        self.url = url
        self.html = None
        self.doc = None
        self.image = ''

        Drag.__init__(self, url)

    # 获取页面
    def _handle(self):
        m = hashlib.md5()
        m.update(self.url)
        file = Config.DIR_PATH + m.hexdigest() + '.txt'
        service_logger.info(data={"url": self.url, "file": file})

        if os.path.exists(file):
            with open(file) as f:
                self.html = f.read()
        else:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                "Referer": self.url
            }
            response = requests.get(self.url, headers=headers)
            service_logger.info(data={"url": self.url, "code": response.status_code, "reason": response.reason})
            self.html = response.content
            with open(file, 'wb') as f:
                f.write(self.html)

        # 转doc对象
        self.doc = pq(self.html)

    # 分类
    def _category(self):
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

                imgs = re.findall('&lt;img src&#x3D;&quot;(.*?)&quot;', content, re.S)
                if len(imgs)>0:
                    self.image = imgs[0]

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
        return self.image










