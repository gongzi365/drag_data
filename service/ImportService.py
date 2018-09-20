# _*_ coding: utf-8 _*_
from service import service_logger
from model.TermRelationshipsModel import TermRelationshipsModel
from model.TermsModel import TermsModel
from model.PostsModel import PostsModel
from model.TermTaxonomyModel import TermTaxonomyModel
from config.Config import Config
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media

import urllib2
import os
import time
import random

class ImportService():

    @staticmethod
    def check_url(url):
        res = PostsModel.check(url)
        if res:
            return True

        return False

    @staticmethod
    def upload_image(image, post_id):
        if image == '':
            return

        print image
        file = time.strftime("%Y%m%d%H%M%S", time.localtime()) + '_' + str(random.randint(10000, 99999))
        subs = image.split('/')[-1]
        exts = subs.split('.')
        ext = 'jpg'
        if len(exts) > 1:
            ext = exts[-1]

        filename = file + '.' + ext
        filepath = Config.DIR_PATH + filename
        response = urllib2.urlopen(image)
        cat_img = response.read()
        with open(filepath, 'wb') as f:
            f.write(cat_img)

        from run import wp
        # prepare metadata
        data = {
            'name': filename,
            'type': ext
        }
        # read the binary file and let the XMLRPC library encode it into base64
        with open(filename, 'rb') as img:
            data['bits'] = xmlrpc_client.Binary(img.read())

        response = wp.call(media.UploadFile(data))
        service_logger.info(data=response)
        if 'id' in response:
            PostsModel.insert_meta(post_id, response['id'])

        return True

    @staticmethod
    def insert_handle(data):
        cates = ['互联网', '技术', 'it', 'IT', 'php', 'python', 'nginx', 'java', 'jquery', 'js', '前端']
        if data['parent'] in cates:
            data['parent'] = 'IT技术'

        # 插入post数据
        ID = PostsModel.insert(data)
        if ID is False:
            service_logger.log('插入失败'+data['url'])

        # 插入图片
        if data['image'] != '':
            ImportService.upload_image(data['image'], ID)

        # 检查分类是否存在
        cate = TermsModel.get(data['parent'],  'category')
        if cate is False:
            cate = {}
            term_id = TermsModel.insert(data['parent'])
            if term_id:
                cate['term_id'] = term_id
                # 插入分类同步记录
                cate['term_taxonomy_id'] = TermTaxonomyModel.insert(cate['term_id'],  'category')

        # 将文章关联分类
        if 'term_taxonomy_id' in cate:
            TermRelationshipsModel.insert(ID, cate['term_taxonomy_id'])
            # 更新统计数据
            TermTaxonomyModel.update_count(cate['term_taxonomy_id'])

        # 检查标签是否存在
        if data['tags'] != '':
            tags = data['tags'].split(',')
            for tag in tags:
                resu = TermsModel.get(tag,  'post_tag')
                if resu is False:
                    resu = {}
                    resu['term_id'] = TermsModel.insert(tag)
                    # 插入分类同步记录
                    resu['term_taxonomy_id'] = TermTaxonomyModel.insert(resu['term_id'],  'post_tag')

                # 将文章关联分类
                if 'term_taxonomy_id' in resu:
                    TermRelationshipsModel.insert(ID, resu['term_taxonomy_id'])
                    # 更新统计数据
                    TermTaxonomyModel.update_count(resu['term_taxonomy_id'])

        return True



