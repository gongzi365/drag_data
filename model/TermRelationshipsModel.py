# _*_ coding: utf-8 _*_
from service.SqlService import SqlService
from service import service_logger

class TermRelationshipsModel():

    @staticmethod
    def insert(object_id, term_taxonomy_id):
        # 插入的sql
        insert_sql = "insert into wp_term_relationships(object_id, term_taxonomy_id) values('{object_id}', '{term_taxonomy_id}')" \
                     .format(object_id=object_id, term_taxonomy_id=term_taxonomy_id)

        service_logger.log(insert_sql)

        res = SqlService.api(insert_sql, 'execute')
        if res is not None:
            return True

        return False
