# _*_ coding:utf-8 _*_
"""
示例配置文件
"""


class Config:
    # ----- 临时操作目录 ----- #
    # DIR_PATH = '/mnt/hgfs/sharedev/drag_data/tmp/'
    DIR_PATH = 'D:/sharedev/drag_data/tmp/'

    # ----- Mysql 配置 ------ #
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@192.168.1.248:3306/anfeng_packet?charset=utf8'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@127.0.0.1:3306/wp_test?charset=utf8'

    # ----- Mysql 调试输出开关 ----- #
    MYSQL_DEBUG = False

    # ----- 日志相关 ----- #
    LOG_TOPIC = 'PACKETLOG'
    # LOG_PATH = '/mnt/hgfs/sharedev/logs/drag.log'
    LOG_PATH = 'D:/sharedev/drag_data/tmp/drag.log'



