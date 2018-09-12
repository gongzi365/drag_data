# _*_ coding: utf-8 _*_
from service import service_logger, mysql_session
from utils.SwitchUtil import switch
from config.Config import Config
import traceback


class SqlService():

    # packet sql
    ARTICLE_LIST = 'select * from wp_article where url = "%s"'


    @staticmethod
    def sql(*args):
        args_len = len(args)
        for case in switch(args_len):
            if case(1):
                _sql = args[0]
                break
            if case(2):
                _sql = args[0] % (args[1])
                break
            if case(3):
                _sql = args[0] % (args[1], args[2])
                break
            if case(4):
                _sql = args[0] % (args[1], args[2], args[3])
                break
            if case(5):
                _sql = args[0] % (args[1], args[2], args[3], args[4])
                break
            if case(6):
                _sql = args[0] % (args[1], args[2], args[3], args[4], args[5])
                break
            if case(7):
                _sql = args[0] % (args[1], args[2], args[3], args[4], args[5], args[6])
                break
            if case(8):
                _sql = args[0] % (args[1], args[2], args[3], args[4], args[5], args[6], args[7])
                break
            if case(9):
                _sql = args[0] % (args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8])
                break
            if case(10):
                _sql = args[0] % (args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8], args[9])
                break

        return _sql

    # anfanapi
    @staticmethod
    def api(sql=None, method='first'):
        try:
            data = None
            for case in switch(method):
                if case('first'):
                    data = mysql_session.execute(sql).first()
                    if data is not None:
                        data = dict(data)
                    break
                if case('scalar'):
                    data = mysql_session.execute(sql).scalar()
                    break
                if case('fetchall'):
                    data = mysql_session.execute(sql).fetchall()
                    break
                if case('execute'):
                    data = mysql_session.execute(sql)
                    mysql_session.commit()
                    break

            # 是否打印日志
            if Config.MYSQL_DEBUG:
                service_logger.warn("sql:api", {"sql": sql})

            return data
        except Exception, err:
            mysql_session.rollback()
            service_logger.error("sql:error", {"sql": sql, "data": traceback.format_exc()})

            return None
        finally:
            mysql_session.close()
