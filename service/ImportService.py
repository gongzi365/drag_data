# _*_ coding: utf-8 _*_
from service import service_logger
from model.TermRelationshipsModel import TermRelationshipsModel
from model.TermsModel import TermsModel
from model.PostsModel import PostsModel
from model.TermTaxonomyModel import TermTaxonomyModel
from config.Config import Config
from resizeimage import resizeimage
from PIL import Image

import urllib2
import requests

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
    def upload_image(image, iscut=False, w=300, h=200):
        if image == '':
            return

        file = time.strftime("%Y%m%d%H%M%S", time.localtime()) + '_' + str(random.randint(10000, 99999))
        subs = image.split('/')[-1]
        exts = subs.split('.')
        ext = 'jpg'
        if len(exts) > 1:
            ext = exts[-1]

        filename = file + '.' + ext
        y = time.strftime("%Y", time.localtime())
        m = time.strftime("%m", time.localtime())
        filepath = Config.IMAGE_PATH + '/' + y + '/' + m
        if os.path.isdir(filepath) == False:
            os.makedirs(filepath, 0775)

        newfile = filepath + '/' + filename
        oldfile = Config.DIR_PATH + filename

        # 存储原图
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36"}
        response = requests.get(image, headers=headers)
        cat_img = response.content
        with open(oldfile, "wb") as f:
            f.write(cat_img)

        if iscut:
            # 存储裁剪图
            with open(oldfile, 'rb') as f:
                with Image.open(f) as img:
                    cover = resizeimage.resize_cover(img, [w, h])
                    cover.save(newfile, img.format)
        else:
            # 存储新的图片
            with open(newfile, 'wb') as f:
                f.write(cat_img)

        # 图片日志
        service_logger.warn(data={"image": image, 'old': oldfile, 'new': newfile})

        # 删除图片
        os.remove(oldfile)

        return y + '/' + m + '/' + filename

    @staticmethod
    def insert_handle(data, type='article'):
        cates = ['技术', 'it', 'IT', 'php', 'python', 'nginx', 'java', 'jquery', 'js', '前端']
        if data['parent'] in cates:
            data['parent'] = '技术'

        if data['parent'] == '其他':
            data['parent'] = '其它'

        # 插入post数据
        if type == 'video':
            ID = PostsModel.insert_video(data)
            width = 480
            height = 320
        else:
            ID = PostsModel.insert(data)
            width = 300
            height = 200
        if ID is False:
            service_logger.log('插入失败'+data['url'])
            return False

        # 插入图片
        if data['image'] != '':
            image = ImportService.upload_image(data['image'], iscut=True, w=width, h=height)
            PostsModel.insert_image(image, ID, data['type'], data['url'])

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



