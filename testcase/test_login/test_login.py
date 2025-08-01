# -*- coding: utf-8 -*-
# @File: test_login.py
# @Time: 2025/7/21 23:05
# @Author: rock
# @Email: 1187338689@qq.com
import sys
import os

# 确保项目根目录在sys.path中，这样可以正确导入项目模块
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

import pytest, allure
from utils.handle_excel import get_excel_data
from utils.handle_path import excel_test_case_path, report_path
from libs.login.login import Login


@allure.epic('权益端')
@allure.feature('登录模块')
@pytest.mark.login # 登录标签
class TestLogin:

    @allure.story('登录接口')
    @allure.title('{title}')
    @pytest.mark.parametrize('title,req_body,resp_data',
                             get_excel_data(excel_test_case_path,"登录模块", "Login"))# , run_case=['001-005']))
    def test_login(self, title, req_body, resp_data):
        res = Login().login(req_body)
        # print(res['nick_name'])
        try:
            assert res['nick_name'] == resp_data
        except:
            assert res['error_description'] == resp_data

if __name__ == '__main__':
    pytest.main([__file__, '--clean-alluredir', '--alluredir', report_path])
    # os.system(f'allure serve {report_path}')