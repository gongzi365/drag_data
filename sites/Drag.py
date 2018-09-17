# _*_ coding: utf-8 _*_
from service import service_logger

import traceback

class Drag(object):

    def __init__(self, url=None):
        service_logger.log('#########开始抓取网页########')
        self.url = url

        self.handle()

    def handle(self):
        service_logger.log(self.url)

        try:
            self._handle()
        except Exception, err:
            service_logger.error("task-exception", {"msg": traceback.format_exc(), "url": self.url})

    def get_content(self):
        data = {
            'platform': self.platform,
            'type': self.type,
            'url': self.url
        }

        # 分类
        cate = self._category()
        if len(cate) == 1:
            data['parent'] = cate[0]
            data['category'] = ''
        elif len(cate) == 2:
            data['parent'] = cate[0]
            data['category'] = cate[1]
        else:
            data['parent'] = '其它'
            data['category'] = ''

        # 标题
        data['title'] = self._title()

        # 内容
        pre = '<strong>【转载】</strong>%s<br /><strong>原文链接：</strong><a href="%s">%s</a>' % (data['title'], self.url, self.url)
        data['content'] = self._content() + pre

        # 标签
        data['tags'] = self._tags()

        # 图片
        data['image'] = self._image()

        # 发布时间
        data['send_time'] = self._send_time()

        return data







