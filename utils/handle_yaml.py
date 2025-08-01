# -*- coding: utf-8 -*-
# @File: handle_yaml.py
# @Time: 2025/7/21 11:28
# @Author: rock
# @Email: 1187338689@qq.com
import yaml
from utils.handle_path import api_config_yaml_path
from utils.logger import log
import traceback  # 最全的报错日志信息


def get_yaml_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f.read())
    except:
        log.error(f"报错信息：{traceback.format_exc()}")

if __name__ == '__main__':
    print(get_yaml_data(api_config_yaml_path))

