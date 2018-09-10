# _*_ coding: utf-8 _*_
from service.SqlService import SqlService
from service import service_logger

class TaskService():

    @staticmethod
    def get(where='status=0'):
        sql = SqlService.sql(SqlService.TASK_LIST, where)
        data = SqlService.api(sql)
        if data is not None and 'task_id' in data:
            return data

        return None

    @staticmethod
    def update(self, up_str='', id=0):
        if up_str == '':
            service_logger.error({"msg": "up_str error", "task_id": id})

        sql = SqlService.sql(SqlService.TASK_UPDATE, up_str, id)
        SqlService.api(sql, 'execute')

        return True



