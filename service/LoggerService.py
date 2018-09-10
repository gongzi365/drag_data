# _*_ coding: utf-8 _*_
import logging
import json

'''
日志级别：
critical > error > warning > info > debug,notset
级别越高打印的日志越少，反之亦然，即
debug    : 打印全部的日志(notset等同于debug)
info     : 打印info,warning,error,critical级别的日志
warning  : 打印warning,error,critical级别的日志
error    : 打印error,critical级别的日志
critical : 打印critical级别
'''

class LoggerService():

    def __init__(self, loglevel, logname, logpath):
        '''
           指定保存日志的文件路径，日志级别，以及调用文件
           将日志存入到指定的文件中
        '''

        # 创建一个logger
        self.logger = logging.getLogger(logname)
        self.logger.setLevel(loglevel)

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(logpath)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s[line:%(lineno)d] - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def getlog(self):
        return self.logger

    def error(self, type='error', data={}):
        str = '['+type+'] '+json.dumps(data, ensure_ascii=False)
        return self.logger.error(str)

    def info(self, type='info', data={}):
        str = '['+type+'] '+json.dumps(data, ensure_ascii=False)
        return self.logger.info(str)

    def warn(self, type='warn', data={}):
        str = '['+type+'] '+json.dumps(data, ensure_ascii=False)
        return self.logger.warning(str)

    def debug(self, type='debug', data={}):
        str = '['+type+'] ' + json.dumps(data, ensure_ascii=False)
        return self.logger.debug(str)

    def log(self, data=''):
        str = '[warn] ' + data
        return self.logger.warning(str)