# -*- coding: utf-8 -*-
# @File: handle_path.py
# @Time: 2025/7/21 11:12
# @Author: rock
# @Email: 1187338689@qq.com
# 通过获取当前环境的地址，避免切换环境后path不对的问题
import os

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 举例
key_path = os.path.join(project_path, "data\\") + "public.pem"
log_save_path = os.path.join(project_path, "outfiles\\logs\\")
api_config_yaml_path = os.path.join(project_path, "configs\\") + "api_config.yaml"
img_code_path = os.path.join(project_path, "case_datas\\") + "code_image.png"
excel_test_case_path = os.path.join(project_path, "data\\") + "testCaseFile.xls"
case_config_path = os.path.join(project_path, "configs\\") + "case_config.yaml"
report_path = os.path.join(project_path, "outfiles\\report\\tmp")
config_path = os.path.join(project_path, "configs\\")


if __name__ == '__main__':
    print(project_path)
    print(api_config_yaml_path)
    print(key_path)
    print(report_path)