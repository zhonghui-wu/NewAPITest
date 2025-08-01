# -*- coding: utf-8 -*-
# @File: supplier_files.py
# @Time: 2025/7/21 11:55
# @Author: rock
# @Email: 1187338689@qq.com
import sys
import os

# 确保项目根目录在sys.path中，这样可以正确导入项目模块
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

from common.base_api import BaseAPI
from libs.login.login import Login
from configs.config import SupplierFilesName



class SupplierFiles(BaseAPI):

    def submit(self, in_data, id = None, image_info = None, supplier_files_name = None):
        # .get方法，如果 key 不存在，返回 None，不会报错
        if in_data.get('id')== '${id}':
            in_data['id'] = id
        if in_data.get('supplierName') == '${SupplierFilesName}':
            in_data['supplierName'] = supplier_files_name
        in_data['image_path'] = image_info
        return super().submit(json=in_data)

    def delete(self, in_data, id = None, supplier_code = None):
        if in_data.get('id') == '${id}':
            in_data['id'] = id
        if in_data.get('supplierCode') == '${supplierCode}':
            in_data['supplierCode'] = supplier_code
        return super().delete(data=in_data)

    def enable(self, in_data, id = None):
        if in_data.get('id') == '${id}':
            in_data['id'] = id
        return super().enable(json=in_data)


if __name__ == '__main__':
    # 1.登录
    payload = {
        "tenantId": "000000",
        "username": "rock",
        "password": "123456",
        "grant_type": "password",
        "scope": "all",
        "type": "account"
    }
    token = Login().login(payload, get_token=True)
    # 2.新增供方档案
    create_data = {"supplierName":"${SupplierFilesName}","contactName":"rock","contactPhone":"13111111111","email":"13111111111@163.com","tenantId":"000000"}
    SupplierFiles(token).submit(create_data, supplier_files_name = SupplierFilesName)
    # # 3.查询供方档案
    # query_data = {"current": 1, "size": 1}
    # id = SupplierFiles(token).list(params = query_data)['data']['records'][0]['id']
    # supplierCode = SupplierFiles(token).list(params=query_data)['data']['records'][0]['supplierCode']
    # print(id)
    # # 4.编辑供方档案
    # create_data = {"supplierName": "${SupplierFilesName}", "contactName": "456", "contactPhone": "13222222222",
    #                "email": "13222222222@163.com", "tenantId": "000000", "id": "${id}"}
    # res = SupplierFiles(token).submit(create_data, id = id, supplier_files_name = SupplierFilesName)
    # print(res)
    # # 5.启用供方
    # on_data = {"id": "${id}","enable":"true"}
    # res = SupplierFiles(token).enable(on_data, id = id)
    # print(res)
    # query_data = {"current": 1, "size": 1}
    # # 6.禁用供方
    # off_data = {"id": "${id}", "enable": "false"}
    # res = SupplierFiles(token).enable(off_data, id=id)
    # print(res)
    # # 7.删除供方档案
    # delete_data = {"id": "${id}","supplierCode": "${supplierCode}"}
    # res = SupplierFiles(token).delete(delete_data, id = id, supplier_code = supplierCode)
    # print(res)