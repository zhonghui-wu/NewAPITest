# -*- coding: utf-8 -*-
# @File: test_supplier_files.py
# @Time: 2025/7/22 15:09
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
from utils.assert_fields import assert_fields_match
from configs.config import AES32_KEY, SupplierFilesName
from utils.get_aes32 import AesUtil


@allure.epic('权益端')
@allure.feature('供方管理--供方档案')
@pytest.mark.supplier_files # 供方档案标签
class TestSupplierFiles:

    @allure.story('查询供方档案接口')
    @pytest.mark.parametrize('title,req_body,resp_data',
                             get_excel_data(excel_test_case_path,"供方管理", "listsupplier"))#, run_case=['002']))
    @allure.title('{title}')
    @pytest.mark.list_supplier_files  # 查询供方档案标签
    def test_list_supplier_files(self, supplier_init, title, req_body, resp_data):
        res = supplier_init.list(params = req_body)
        # print(res)
        # print(resp_data)
        try:
            if req_body['contactPhone']:
                for one in res['data']['records']:
                    # 用例中resp_data的手机号加密
                    one['contactPhone'] = AesUtil.decrypt_from_base64(one['contactPhone'], AES32_KEY)
        except:
            pass
        try:
            if res['data']['records']:
                # print(res['data']['records'])
                # try:
                # 模糊匹配res['data']['records']中包含了resp_data数据
                assert_fields_match(res['data']['records'], resp_data)
                # except:
                    # print(len(res['data']['records']))
                    # assert len(res['data']['records']) == resp_data or res['data']['records'] == resp_dat

        except:
            # 断言res是否包含了resp_data里面的键值对数据
            # assert resp_data.keys() <= res.keys() and all(res[k] == v for k, v in resp_data.items())
            assert_fields_match(res, resp_data)


    @allure.story('创建/编辑供方档案接口')
    @pytest.mark.parametrize('title,req_body,resp_data',
                             get_excel_data(excel_test_case_path, "供方管理", "submitsupplier"))#, run_case=['002']))
    @allure.title('{title}')
    @pytest.mark.submit_supplier_files  # 创建/编辑供方档案标签
    def test_submit_supplier_files(self, supplier_init, title, req_body, resp_data, delete_suppliers_files):
        # print(resp_data)

        with allure.step('查询需要编辑的供方档案id'):
            body = {"current": 1, "size": 1}
            supplier_files_id = supplier_init.list(params=body)['data']['records'][0]['id']
        with allure.step('执行启用/禁用用例'):
            # print(req_body)
            res = supplier_init.submit(req_body, id = supplier_files_id, supplier_files_name = SupplierFilesName)
            # print(res)
        with allure.step('断言'):
            assert_fields_match(res, resp_data)
            # assert res == resp_data


    @allure.story('启用禁用供方档案接口')
    @pytest.mark.parametrize('title,req_body,resp_data',
                             get_excel_data(excel_test_case_path, "供方管理", "enablesupplier"))  # , run_case=['023']))
    @allure.title('{title}')
    @pytest.mark.enable_supplier_files  # 启用/禁用供方档案标签
    def test_enable_supplier_files(self, supplier_init, title, req_body, resp_data):
        # print(resp_data)

        with allure.step('查询需要启用/禁用的供方档案id'):
            body = {"current":1,"size":1}
            supplier_files_id = supplier_init.list(params = body)['data']['records'][0]['id']
        with allure.step('执行启用/禁用用例'):
            res = supplier_init.enable(req_body, id = supplier_files_id)
            # print(res)
        with allure.step('断言'):
            assert_fields_match(res, resp_data)
            # assert res == resp_data




    @allure.story('删除供方档案接口')
    @pytest.mark.parametrize('title,req_body,resp_data',
                             get_excel_data(excel_test_case_path, "供方管理", "deletesupplier"), ids=ids)#  , run_case=['001']))
    @allure.title('{title}')
    @pytest.mark.delete_supplier_files  # 删除供方档案标签
    def test_delete_supplier_files(self, supplier_init, title, req_body, resp_data, create_suppliers_files):
        # print(resp_data)

        with allure.step('查询需要删除的供方档案id'):
            body = {"supplierName":"rock自动化测试供方档案","current":1,"size":1}
            supplier_files_id = supplier_init.list(params = body)['data']['records'][0]['id']
            supplier_code = supplier_init.list(params = body)['data']['records'][0]['supplierCode']
        with allure.step('执行启用/禁用用例'):
            res = supplier_init.delete(req_body, id = supplier_files_id, supplier_code = supplier_code)
            # print(res)
        with allure.step('断言'):
            assert_fields_match(res, resp_data)
            # assert res == resp_data





if __name__ == '__main__':
    pytest.main([__file__, '-s',  '-m', 'submit_supplier_files', '--clean-alluredir', '--alluredir', report_path])
    # pytest.main([__file__, '--clean-alluredir', '--alluredir', report_path])
    # os.system(f'allure serve {report_path}')