#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# --encoding:utf-8--
# -*- coding: UTF-8 –*-
'''
# @see http://c.isme.pub/2018/01/18/python-logging/

"""
logging配置
"""
import os
import time
import logging.config

# 定义三种日志输出格式 开始
standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
                  '[%(levelname)s][%(message)s]'  # 其中name为getlogger指定的名字
simple_format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
id_simple_format = '[%(levelname)s][%(asctime)s] %(message)s'

# 定义日志输出格式 结束
logfile_dir = os.path.dirname(os.path.abspath(__file__))  # log文件的目录
# 如果不存在定义的日志目录就创建一个
if not os.path.isdir(logfile_dir):
    os.mkdir(logfile_dir)


def load_my_logging_cfg(logfileName):
    if(logfileName == ''):
        logfile_name = 'all_with_logging.log'  # log文件名
    else:
        logfile_name = logfileName
    # log文件的全路径
    logfile_path = os.path.join(logfile_dir, logfile_name)
    logfile_name = logfileName
    # log配置字典
    LOGGING_DIC = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': standard_format
            },
            'simple': {
                'format': simple_format
            },
        },
        'filters': {},
        'handlers': {
            # 打印到终端的日志
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',  # 打印到屏幕
                'formatter': 'simple'
            },
            # 打印到文件的日志,收集info及以上的日志
            'default': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
                'formatter': 'standard',
                'filename': logfile_path,  # 日志文件
                'maxBytes': 1024*1024*5,  # 日志大小 5M
                'backupCount': 5,
                'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
            },
        },
        'loggers': {
            # logging.getLogger(__name__)拿到的logger配置
            '': {
                # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
                'handlers': ['default', 'console'],
                'level': 'DEBUG',
                'propagate': True,  # 向上（更高level的logger）传递
            },
        },
    }
    logging.config.dictConfig(LOGGING_DIC)  # 导入上面定义的logging配置


def demoForTest():
    logger = logging.getLogger(__name__)  # 生成一个log实例
    logger.info('logging setting It is works!')  # 记录该文件的运行状态
    logger.debug("start range... time:{}".format(time.time()))
    logger.info(u"中文测试开始。。。")
    for i in range(10):
        logger.debug("中文 i:{}".format(i))
        time.sleep(0.2)
    else:
        logger.debug("over range... time:{}".format(time.time()))
    logger.info(u"中文测试结束。。。")


if __name__ == '__main__':
    load_my_logging_cfg('all.log')
    demoForTest()
