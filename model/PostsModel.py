# _*_ coding: utf-8 _*_
from service.SqlService import SqlService
from service import service_logger
from config.Config import Config

import time
import urllib
import random

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
        # post_name = urllib.quote(data['title'].encode('utf8'))
        post_name = data['title']

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
                    post_name=post_name, from_type=data['type'], from_url=data['url'],
                    from_ctime=data['send_time'])

        # 打印sql
        # service_logger.log(insert_sql)

        res = SqlService.api(insert_sql, 'execute')
        if res is not None:
            # 插入浏览数
            views_count = random.randint(1, 200)
            insert_meta_sql = "insert into wp_postmeta(post_id, meta_key, meta_value) value (%s, 'post_views_count', '%s')" % (res, views_count)
            service_logger.log(insert_meta_sql)
            SqlService.api(insert_meta_sql, 'execute')

            return res

        return False

    @staticmethod
    def insert_meta(post_id, attachment_id):
        insert_meta_sql = "insert into wp_postmeta(post_id, meta_key, meta_value) value (%s, '_thumbnail_id', '%s')" % (post_id, attachment_id)
        service_logger.log(insert_meta_sql)
        res = SqlService.api(insert_meta_sql, 'execute')
        if res is not None:
            return res

        return False

    @staticmethod
    def insert_image(image, post_id, from_type, from_url):
        post_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        content = ''
        post_name = 'origin_'+time.strftime("%Y%m%d%H%M%S", time.localtime())+str(random.randint(10000, 99999))
        guid = Config.BASE_URL + 'wp-content/uploads/' + image
        mime_type = 'image/' + guid.split('.')[-1]

        # 插入的sql
        insert_sql = "insert into wp_posts(post_author, post_date, post_date_gmt, " \
                                 " post_excerpt, to_ping, pinged, post_content_filtered, " \
                                 " post_title, post_content, post_status,comment_status, ping_status, " \
                                 " post_name, post_type, from_type, from_url, " \
                                 " post_parent, guid, post_mime_type)" \
                                 " values('1', '{post_date}', '{post_date_gmt}'," \
                                 "  '', '', '', '', " \
                                 " '{title}', '{content}', 'inherit', 'open', 'closed', " \
                                 " '{post_name}', 'attachment', '{from_type}', '{from_url}', " \
                                 " '{post_parent}', '{guid}', '{mime_type}')" \
                        .format(post_author=1, post_date=post_date, post_date_gmt=post_date,
                                    title=post_name, content=content,
                                    post_name=post_name, from_type=from_type, from_url=from_url,
                                    post_parent=post_id, guid=guid, mime_type=mime_type)

        # 打印sql
        # service_logger.log(insert_sql)
        res = SqlService.api(insert_sql, 'execute')
        if res is not None:
            insert_meta1_sql = "insert into wp_postmeta(post_id, meta_key, meta_value) value (%s, '_wp_attached_file', '%s')" % (res, image)
            service_logger.log(insert_meta1_sql)
            SqlService.api(insert_meta1_sql, 'execute')

            insert_meta2_sql = "insert into wp_postmeta(post_id, meta_key, meta_value) value (%s, '_thumbnail_id', '%s')" % (post_id, res)
            service_logger.log(insert_meta2_sql)
            SqlService.api(insert_meta2_sql, 'execute')

            return res

        return False







