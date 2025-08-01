# -*- coding: utf-8 -*-
# @File: config.py
# @Time: 2025/7/21 11:19
# @Author: rock
# @Email: 1187338689@qq.com
import time
HOST = "https://5r5152q357.goho.co/right/api"
ONLINE_HOST = "https://right.rayoservice.com/api"
LOGIN_HEADER = {
        "Tenant-Id": "000000",
        "Authorization": "hmqw/gbbTD6fgjOuV+VchuiLtOzskNBofbYMmRP2wMy6bZeFqhZ7Rbq6C8U6WqPiy3PUp3Pzaod0ELTU21iO54Mb"
                         "Zs4HJTdND79t2Mqk3vuTGeF81o4gYJC4DsZyjCwsT/mn0tOd60fSniwO/By71T1er1VbGU2WOneIiefb4oY=",
        "Content-Type": "application/json;charset=UTF-8"
    }
LOGIN_PAYLOAD = {
        "tenantId": "000000",
        "username": "rock",
        "password": "123456",
        "grant_type": "password",
        "scope": "all",
        "type": "account"
               }

AES32_KEY = "eEQ87QBQEed86y91c6kTwRZ9xBuDItL1"
SupplierFilesName = "rock自动化测试供方档案"  + str(int(time.time()))[-6:]
