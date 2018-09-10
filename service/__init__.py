# _*_ coding: utf-8 _*_
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import SingletonThreadPool

from config.Config import Config
from service.LoggerService import LoggerService

import logging

# 初始化日志模块
service_logger = LoggerService(logging.DEBUG, Config.LOG_TOPIC, Config.LOG_PATH)

# 连接数据库
mysql_engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, encoding="utf-8",
                                 echo=Config.MYSQL_DEBUG,
                                 pool_recycle=28800, poolclass=SingletonThreadPool)

mysql_session = sessionmaker(autocommit=False, bind=mysql_engine)()

