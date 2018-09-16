# _*_ coding: utf-8 _*_
from service.SqlService import SqlService
from service import service_logger

class TermTaxonomyModel():

    @staticmethod
    def insert(term_id, taxonomy='post_tag'):
        # taxonomy=post_tag,category
        # 插入的sql
        insert_sql = "insert into wp_term_taxonomy(term_id, taxonomy, description) values('{term_id}', '{taxonomy}', '')" \
                                    .format(term_id=term_id, taxonomy=taxonomy)

        service_logger.log(insert_sql)

        res = SqlService.api(insert_sql, 'execute')
        if res is not None:
            return res

        return False

    @staticmethod
    def update_count(term_taxonomy_id):

        update_sql = SqlService.sql(SqlService.UPDATE_TERM_TAXONOMY, term_taxonomy_id)
        res = SqlService.api(update_sql, 'execute')
        if res is not None:
            return res

        return False
