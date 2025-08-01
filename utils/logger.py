# -*- coding: utf-8 -*-
# @File: logger.py
# @Time: 2025/7/21 17:14
# @Author: rock
# @Email: 1187338689@qq.com
from configparser import ConfigParser
from loguru import  logger
from utils.handle_path import log_save_path, config_path
from time import strftime
import os, logging


class PropogateHandler(logging.Handler):
    def emit(self, record):
        logging.getLogger(record.name).handle(record)


class MyLog():
    __instance = None # 单例实现
    __call_flag = True # 控制init调用，如果调用过就不再调用

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def get_log(self):
        if self.__call_flag:
            # 获取当前日期
            __curdate = strftime('%Y%m%d-%H%M%S')

            # 配置文件读取
            cfg = ConfigParser()
            cfg.read(os.path.join(config_path, 'loguru.ini'), encoding='utf-8')

            # 移除现有 handler，关闭console输出
            logger.remove(handler_id=None)

            # 添加新的日志文件路径
            logger.add(os.path.join(log_save_path, 'quanyiduan_') + __curdate + '.log', encoding='utf8',  # 日志存放位置
                       retention=cfg.get(section='log', option='retention'),  # 清理
                       rotation=cfg.get(section='log', option='rotation'),  # 轮转
                       format=cfg.get(section='log', option='format'),  # 日志输出格式
                       compression=cfg.get(section='log', option='compression'),  # 日志压缩格式
                       level=cfg.get(section='log', option='level'))  # 日志级别

            logger.add(PropogateHandler())  # 添加自定义的日志处理器
            self.__call_flag = False  # 防止重复调用

            return logger

log = MyLog().get_log()

if __name__ == '__main__':
    log.error('testing')

