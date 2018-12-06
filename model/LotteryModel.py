# _*_ coding: utf-8 _*_
from service.SqlService import SqlService
from service import service_logger

import time

class LotteryModel():

    @staticmethod
    def get_list(where, limit=20):

        sql = SqlService.sql(SqlService.LOTTERY_LIST, where, limit)
        print sql
        resu = SqlService.api(sql, 'fetchall')
        if resu is not None:
            return resu

        return False


    @staticmethod
    def update_lottery(where, real, yuce):

        sql = SqlService.sql(SqlService.UPDATE_lOTTERY, real, yuce, where)
        res = SqlService.api(sql, 'execute')
        if res is not None:
            return True

        return False







