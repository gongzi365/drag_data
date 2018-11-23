# _*_ coding: utf-8 _*_
from Drag import Drag
from pyquery import PyQuery as pq
from utils.Helper import *
from service import service_logger

import re
import json

class Dytt(Drag):
    platform = '电影天堂'
    type = 'dytt'

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
            if html != '':
                self.html = html.decode('gb18030', 'ignore').encode('utf-8', 'ignore')
                write_file(self.url, self.html)
            else:
                self.html = ''

        # 转doc对象
        self.doc = pq(self.html)
        self.cate = []
        self.title = ''
        self.send_time = ''
        self.tags = ''

    def set_category(self, cate):
        self.cate = cate

    # 分类
    def _category(self):

        return self.cate

    # 标题
    def _title(self):
        title = ''
        resu = re.findall('<div class="title_all"><h1><font .*?>(.*?)</font>', self.html, re.S)
        if len(resu) > 0:
            title = resu[0]
        return title

    # 内容
    def _content(self):
        content = ''
        resu = re.findall('<div id="Zoom">(.*?)</div>', self.html, re.S)
        if len(resu) > 0:
            content = resu[0].strip()
            resu1 = re.findall('发布时间：(.*?)\s', content, re.S)
            if len(resu1) > 0:
                content = content.replace('发布时间：'+resu1[0], '')
                content = content.strip()

            content = content.replace('<script language=javascript src="/js1/750.js"></script>', '')
            content = content.replace('www.ygdy8.com', 'v.media88.cn')

            index = content.find('<br><center>')
            length = len(content)
            if index > 0:
                content = content[0:index]

        return content

    # 标签
    def _tags(self):
        tag = ''
        resu = re.findall('◎类　　别(.*?)<br />', self.html, re.S)
        if len(resu) > 0:
            tag = resu[0].strip()
            tag = tag.replace('　', '')
            tag = tag.replace('/', ',')
            tag = tag.replace('\\', ',')
            tag = tag.strip()

        return tag

    # 图片
    def _image(self):
        image = ''
        imgs = re.findall('<img border="0".*?src="(.*?)"', self.html, re.S)
        if len(imgs) > 0:
            image = imgs[0]

        return image

    # 发布时间
    def _send_time(self):
        send_time = ''
        resu = re.findall('发布时间：(.*?)\s', self.html, re.S)
        if len(resu) > 0:
            send_time = resu[0] + ' 0:0:0'

        return send_time

    # 其它数据
    def _others(self):
        others = {
            "name": "",
            "name_cn": "",
            "year": "",
            "country": "",
            "language": "",
            "font": "",
            "release_date": "",
            "score": "",
            "file_size": "",
            "movie_duration": "",
            "director": "",
            "actors": "",
        }

        fields = {
            'name_cn': '◎译　　名(.*?)<br />',
            'name': '◎片　　名(.*?)<br />',
            'year': '◎年　　代(.*?)<br />',
            'country': '◎(产　　地|国　　家)(.*?)<br />',
            'category': '◎类　　别(.*?)<br />',
            'language': '◎语　　言(.*?)<br />',
            'font': '◎字　　幕(.*?)<br />',
            'release_date': '◎上映日期(.*?)<br />',
            'score': '◎(IMDB评分|豆瓣评分)(.*?)<br />',
            'file_size': '◎文件大小(.*?)<br />',
            'movie_duration': '◎片　　长(.*?)<br />',
            'director': '◎导　　演(.*?)<br />',
            'actors': '◎主　　演(.*?)<br />',
        }

        for key, regex in fields.items():
            try:
                resu = re.findall(regex, self.html, re.S)
                if len(resu) > 0:
                    if type(resu[0]).__name__ == 'tuple':
                        value = resu[0][1]
                    else:
                        value = resu[0]
                    # 评分
                    if key == 'score' and '/' in value:
                        value = value.split('/')[0]
                    value = value.replace('&nbsp;', '')
                    value = value.replace("\s", '')
                    value = value.replace("　", '')
                    value = value.strip()
                    others[key] = value

            except Exception as e:
                service_logger.log(key + ':' + regex)
                service_logger.log('except:' + repr(e))

        return others












