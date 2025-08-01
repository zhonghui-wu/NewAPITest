# -*- coding: utf-8 -*-
# @File: get_aes32.py
# @Time: 2025/7/29 11:51
# @Author: rock
# @Email: 1187338689@qq.com

from Crypto.Cipher import AES
import base64
import os

# 默认编码
DEFAULT_ENCODING = 'utf-8'

# PKCS7 编码与解码（自定义 BLOCK_SIZE = 32）
class Pkcs7Encoder:
    BLOCK_SIZE = 32

    @staticmethod
    def encode(data: bytes) -> bytes:
        pad_len = Pkcs7Encoder.BLOCK_SIZE - (len(data) % Pkcs7Encoder.BLOCK_SIZE)
        padding = bytes([pad_len] * pad_len)
        return data + padding

    @staticmethod
    def decode(data: bytes) -> bytes:
        pad_len = data[-1]
        if pad_len < 1 or pad_len > Pkcs7Encoder.BLOCK_SIZE:
            return data
        return data[:-pad_len]

# AES 加解密工具
class AesUtil:
    @staticmethod
    def gen_aes_key() -> str:
        return os.urandom(32).hex()

    @staticmethod
    def encrypt(content: str, aes_text_key: str) -> bytes:
        return AesUtil.encrypt_bytes(content.encode(DEFAULT_ENCODING), aes_text_key)

    @staticmethod
    def encrypt_bytes(content: bytes, aes_text_key: str) -> bytes:
        aes_key = aes_text_key.encode(DEFAULT_ENCODING)
        assert len(aes_key) == 32, "aesKey must be 32 bytes long"
        iv = aes_key[:16]
        cipher = AES.new(aes_key, AES.MODE_CBC, iv)
        padded_data = Pkcs7Encoder.encode(content)
        return cipher.encrypt(padded_data)

    @staticmethod
    def encrypt_to_base64(content: str, aes_text_key: str) -> str:
        encrypted = AesUtil.encrypt(content, aes_text_key)
        return base64.b64encode(encrypted).decode()

    @staticmethod
    def encrypt_to_hex(content: str, aes_text_key: str) -> str:
        encrypted = AesUtil.encrypt(content, aes_text_key)
        return encrypted.hex()

    @staticmethod
    def decrypt_from_base64(content: str, aes_text_key: str) -> str:
        encrypted_bytes = base64.b64decode(content)
        return AesUtil.decrypt_to_string(encrypted_bytes, aes_text_key)

    @staticmethod
    def decrypt_from_hex(content: str, aes_text_key: str) -> str:
        encrypted_bytes = bytes.fromhex(content)
        return AesUtil.decrypt_to_string(encrypted_bytes, aes_text_key)

    @staticmethod
    def decrypt_to_string(encrypted: bytes, aes_text_key: str) -> str:
        decrypted = AesUtil.decrypt_bytes(encrypted, aes_text_key)
        return decrypted.decode(DEFAULT_ENCODING)

    @staticmethod
    def decrypt_bytes(encrypted: bytes, aes_text_key: str) -> bytes:
        aes_key = aes_text_key.encode(DEFAULT_ENCODING)
        assert len(aes_key) == 32, "aesKey must be 32 bytes long"
        iv = aes_key[:16]
        cipher = AES.new(aes_key, AES.MODE_CBC, iv)
        decrypted_padded = cipher.decrypt(encrypted)
        return Pkcs7Encoder.decode(decrypted_padded)


if __name__ == '__main__':
    key = "eEQ87QBQEed86y91c6kTwRZ9xBuDItL1"  # 必须是32字节
    text = "13012345678"

    # 加密
    b64 = AesUtil.encrypt_to_base64(text, key)
    print("加密后（Base64）:", b64)

    # 解密
    plain = AesUtil.decrypt_from_base64(b64, key)
    print("解密后:", plain)


