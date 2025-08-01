# -*- coding: utf-8 -*-
# @File: conftest.py
# @Time: 2025/7/26 10:45
# @Author: rock
# @Email: 1187338689@qq.com
import pytest,time
from libs.login.login import Login
from libs.supplier_manage.supplier_files import SupplierFiles
from configs.config import LOGIN_PAYLOAD, SupplierFilesName
from utils.logger import log
import traceback  # 最全的报错日志信息


@pytest.fixture(scope='session', autouse=True)
def running_start():
    print("------自动化测试用例开始执行------")

# 前置登录，获取token
@pytest.fixture(scope='session')
def login_init():
    token = Login().login(LOGIN_PAYLOAD, get_token=True)
    yield token
    # 后面可以继续写数据库清楚和退出登录


@pytest.fixture(scope='session')
def supplier_init(login_init):
    supplier = SupplierFiles(login_init)
    yield supplier


# 解决终端打印乱码
def pytest_collection_modifyitems(items):
    for item in items:
        item.name = item.name.encode('utf-8').decode('unicode-escape') # 修改用例的名字的编码
        item._nodeid = item._nodeid.encode('utf-8').decode('unicode-escape') # 修改用例的提示的编码


# 这里创建4条供方档案用于删除成功的用例有四条
@pytest.fixture(scope='module')
def create_suppliers_files(supplier_init):
    create_data = {"supplierName": "${SupplierFilesName}", "contactName": "rock",
                   "contactPhone": "13111111111", "email": "13111111111@163.com", "tenantId": "000000"}

    for i in range(4):
        supplier_init.submit(create_data, supplier_files_name=SupplierFilesName)
    print('供方档案测试数据4条创建成功')


# 这里删除创建用例增加的供方档案
@pytest.fixture(scope='module')
def delete_suppliers_files(supplier_init):
    list_body = {"supplierName": "rock自动化测试供方档案", "current": 1, "size": 30}
    yield
    res = supplier_init.list(params=list_body)['data']['records']
    for msg in res:
        id = msg['id']
        supplier_code = msg['supplierCode']
        delete_body = {"supplierCode": supplier_code, "id": id}
        supplier_init.delete(delete_body, supplier_code=supplier_code)
        print(f'供方档案{id}删除成功')


