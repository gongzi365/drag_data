# _*_ coding: utf-8 _*_
from service.SqlService import SqlService
from service import service_logger

import time
import urllib

class PostsModel():

    @staticmethod
    def check(url):

        sql = SqlService.sql(SqlService.POSTS_LIST, url)
        resu = SqlService.api(sql)

        if resu is not None and 'ID' in resu:
            return resu

        return False


    @staticmethod
    def insert(data):
        post_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        content = data['content'].replace("'", "\'")

        # 插入的sql
        insert_sql = "insert into wp_posts(post_author, post_date, post_date_gmt, " \
                                 " post_excerpt, to_ping, pinged, post_content_filtered, " \
                                 " post_title, post_content, post_status,comment_status, ping_status, " \
                                 " post_name, post_type, from_type, from_url, from_ctime)" \
                                 " values('1', '{post_date}', '{post_date_gmt}'," \
                                 "  '', '', '', '', " \
                                 " '{title}', '{content}', 'publish', 'open', 'open', " \
                                 " '{post_name}', 'post', '{from_type}', '{from_url}', '{from_ctime}')" \
            .format(post_author=1, post_date=post_date, post_date_gmt=post_date,
                    title=data['title'], content=content,
                    post_name=data['title'], from_type=data['type'], from_url=data['url'],
                    from_ctime=data['send_time'])

        # 打印sql
        # service_logger.log(insert_sql)

        res = SqlService.api(insert_sql, 'execute')
        if res is not None:
            return res

        return False







