# _*_ coding: utf-8 _*_
from service import service_logger
from service.TaskService import TaskService

class ApiException(Exception):

    def __init__(self, message, code=400, data=None):
        Exception.__init__(self, message)

        self.code = code
        self.msg = message
        self.data = data

    def __str__(self):
        return self.msg

    def to_dict(self):
        res = dict(self.data or ())
        res['msg'] = self.msg
        res['code'] = self.code

        return res


def error_handle(msg='', data=None):
    service_logger.error(data={"msg": msg, "data": data})
    raise ApiException(msg)