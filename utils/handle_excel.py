# -*- coding: utf-8 -*-
# @File: handle_excel.py
# @Time: 2025/7/21 20:01
# @Author: rock
# @Email: 1187338689@qq.com
import json
from utils.handle_path import excel_test_case_path, case_config_path
from utils.handle_yaml import get_yaml_data
import xlrd
from utils.logger import log
import traceback  # 最全的报错日志信息

def get_excel_data(file_path, sheet_name, case_name, *cols_name, run_case=None):
    try:
        res_list = []
        # 将cols_name放到case_config.yaml中配置使用，减少这个函数传参
        case_config_data = get_yaml_data(case_config_path)
        cols_name = case_config_data['cols']

        wb = xlrd.open_workbook(file_path, formatting_info=True) # 打开excel
        sheet = wb.sheet_by_name(sheet_name) # 选择对应的sheet
        col_index = []
        for col in cols_name:
            col_index.append(sheet.row_values(0).index(col)) # 通过列名去判断下标，然后将下标数据存到col_index

    # --------------用例筛选---------------
        run_list = [] # 最终执行的用例
        if run_case == None: # 默认全部允许
            run_list = sheet.col_values(0)
        else:
            for case in run_case: # 有两种['001', '002-005']
                if '-' in case:
                    start, end = case.split('-')
                    for i in range(int(start), int(end) + 1):
                        run_list.append(f'{case_name}{i:0>3}') # 补两个0
                else:
                    run_list.append(f'{case_name}{case:0>3}')
        # print('筛选出来要执行的用例：', run_list)

    # ----------------end----------------
        row_index = 0 # 行数据
        for one in sheet.col_values(0): # 第0列每个数据
            if case_name in one and one in run_list:
                cols_data = []
                for num in col_index:
                    tmp = is_json(sheet.cell_value(row_index, num))
                    cols_data.append(tmp) # 每一个所有需要获取的单元格数据
                res_list.append(tuple(cols_data)) # [(行数据1),(行数据2)]
            row_index += 1
        return res_list
    except:
        log.error(f"报错信息：{traceback.format_exc()}")

def is_json(data):
    try:
        return json.loads(data)
    except:
        return data


if __name__ == '__main__':
    rep = get_excel_data(excel_test_case_path, "登录模块", "Login", run_case=['001','004-005'])
    for one in rep:
        print(one)