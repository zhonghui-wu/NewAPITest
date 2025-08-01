# -*- coding: utf-8 -*-
# @File: get_rsa_data.py
# @Time: 2025/7/21 17:07
# @Author: rock
# @Email: 1187338689@qq.com
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64
from utils.handle_path import key_path


def rsa_encrypt(data):
    with open(key_path, 'r', encoding="utf-8") as public:
        key = public.read()
    rsa_key = RSA.importKey(key)  # 导入读取到的公钥
    cipher = PKCS1_v1_5.new(rsa_key)  # 生成对象
    # 通过生成的对象加密message明文，注意，在python3中加密的数据必须是bytes类型的数据，不能是str类型的数据
    cipher_text = base64.b64encode(cipher.encrypt(data.encode("utf-8")))
    return cipher_text.decode("utf-8")


if __name__ == '__main__':
    print(rsa_encrypt("123456"))