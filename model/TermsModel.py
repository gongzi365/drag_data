# _*_ coding: utf-8 _*_
from service.SqlService import SqlService
from service import service_logger

import urllib

class TermsModel():

    @staticmethod
    def get(name, taxonomy='category'):

        sql = SqlService.sql(SqlService.TERMS_LIST, name, taxonomy)
        resu = SqlService.api(sql)

        if resu is not None and 'term_id' in resu:
            return resu

        return False

    @staticmethod
    def insert(name):
        slug = urllib.quote(name.encode('utf8'))

        # 插入的sql
        insert_sql = "insert into wp_terms(name, slug) values('{name}', '{slug}')" \
                     .format(name=name, slug=slug)

        service_logger.log(insert_sql)

        res = SqlService.api(insert_sql, 'execute')
        if res is not None:
            return res

        return False
