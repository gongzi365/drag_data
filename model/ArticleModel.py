# _*_ coding: utf-8 _*_
from service.SqlService import SqlService
from service import service_logger

import time

class ArticleModel():

    @staticmethod
    def check(url):

        sql = SqlService.sql(SqlService.ARTICLE_LIST, url)
        resu = SqlService.api(sql)

        if resu is not None and 'id' in resu:
            return True

        return False


    @staticmethod
    def insert(data):
        create_ts = int(time.time())
        # 插入的sql
        insert_sql = "insert into wp_article(type, parent, category, " \
                                 " title, content, tags, " \
                                 " image, send_time, url, create_time)" \
                                 " values('{type}', '{parent}', '{category}', '{title}', '{content}', '{tags}', " \
                                 " '{image}', '{send_time}', '{url}', {create_time})" \
            .format(type=data['type'], parent=data['parent'], category=data['category'],
                    title=data['title'], content=data['content'], tags=data['tags'],
                    image=data['image'], send_time=data['send_time'], url=data['url'],
                    create_time=create_ts)

        # 打印sql
        service_logger.log(insert_sql)

        res = SqlService.api(insert_sql, 'execute')
        if res is not None:
            return True

        return False







