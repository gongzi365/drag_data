# _*_ coding: utf8 _*_
from service import service_logger
from config.Config import Config
from requests.exceptions import ReadTimeout

import requests
import time
import hashlib
import os

# 获取当前时间戳
def get_current_timestamp():
    return int(time.time())

# 获取网页内容
def get_url_html(url, cookie=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36",
        "Referer": url,
    }
    if cookie is not None:
        headers['cookie'] = cookie

    try:
        response = requests.get(url, headers=headers, timeout=15)
        service_logger.info(data={"url": url, "code": response.status_code, "reason": response.reason, "encoding": response.encoding})
        return response.content
    except ReadTimeout:
        service_logger.info(data={"url": url, "code": '', "reason": 'timeout', "encoding": ''})
        return ''

# 读文件
def read_file(url, ext='.txt'):
    m = hashlib.md5()
    m.update(url)
    file = Config.DIR_PATH + m.hexdigest() + ext
    with open(file) as f:
        content = f.read()

    return content

# 写文件
def write_file(url, html=None, ext='.txt'):
    m = hashlib.md5()
    m.update(url)
    file = Config.DIR_PATH + m.hexdigest() + ext
    with open(file, 'wb') as f:
        f.write(html)

# 删除文件
def delete_file(url, ext='.txt'):
    m = hashlib.md5()
    m.update(url)
    file = Config.DIR_PATH + m.hexdigest() + ext
    if os.path.exists(file):
        os.remove(file)

# 检查是否存在
def check_file(url, ext='.txt'):
    m = hashlib.md5()
    m.update(url)
    file = Config.DIR_PATH + m.hexdigest() + ext
    if os.path.exists(file):
        return True
    else:
        return False







