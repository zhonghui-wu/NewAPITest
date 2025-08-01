# -*- coding: utf-8 -*-
# @File: test_login.py
# @Time: 2025/7/21 11:49
# @Author: rock
# @Email: 1187338689@qq.com

from common.base_api import BaseAPI
from utils.get_rsa_data import rsa_encrypt



class Login(BaseAPI):

    def login(self, in_data, get_token=False):
        in_data['password'] = rsa_encrypt(in_data['password']) # 密码加密
        resp = self.request_send(params=in_data)
        # print(resp)
        if get_token:
            return resp['access_token']
        return resp


if __name__ == '__main__':
    payload = {
        "tenantId": "000000",
        "username": "rock",
        "password": "123456",
        "grant_type": "password",
        "scope": "all",
        "type": "account"
               }
    resp = Login().login(payload, get_token=True)
    print(resp)