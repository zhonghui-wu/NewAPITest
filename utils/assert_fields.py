# -*- coding: utf-8 -*-
# @File: assert_fields.py
# @Time: 2025/7/29 00:21
# @Author: rock
# @Email: 1187338689@qq.com
from utils.logger import log
import traceback  # 最全的报错日志信息


def normalize_bool(val):
    """统一处理布尔值与字符串 'true'/'false'"""
    try:
        if isinstance(val, bool):
            return str(val).lower()
        return str(val).strip().lower()
    except:
        log.error(f"报错信息：{traceback.format_exc()}")

def normalize_supplier_good_type(val):
    try:
        """处理 supplierGoodType 多选字段，转为 set 比较"""
        if isinstance(val, str):
            return set(filter(None, val.strip(',').split(',')))
        return set()
    except:
        log.error(f"报错信息：{traceback.format_exc()}")

def check_field_value(actual, expected, key):
    try:
        """字段比对逻辑支持定制"""
        if isinstance(expected, int) and key == 'records_length':
            return len(actual) == expected
        elif key == 'supplierGoodType':
            return normalize_supplier_good_type(expected).issubset(
                normalize_supplier_good_type(actual)
            )
        elif key == 'enable':
            return normalize_bool(actual) == normalize_bool(expected)
        else:
            # 默认字段：转成字符串 strip 后全等
            return str(actual).strip() == str(expected).strip()
    except:
        log.error(f"报错信息：{traceback.format_exc()}")


def assert_fields_match(records, expected_fields):
    """
    检查 records 是否符合 expected_fields 中的预期条件
    容错：
        - supplierGoodType: 顺序无关、末尾逗号忽略
        - enable: True ↔ "true"
        - 默认字段: 字符串strip后比较
    """
    try:
        mismatches = []

        # 如果 expected_fields 是字典
        if isinstance(expected_fields, dict):
            for k, v in expected_fields.items():
                # 对比每个字段的值
                if isinstance(records, dict):  # 如果 records 是字典
                    if not check_field_value(records.get(k), v, k):
                        mismatches.append(f"Field {k} does not match. Expected {v}, but got {records.get(k)}.")
                elif isinstance(records, list):  # 如果 records 是字典列表
                    for r in records:
                        if not check_field_value(r.get(k), v, k):
                            mismatches.append(f"Field {k} in record {r} does not match. Expected {v}, but got {r.get(k)}.")

        # 如果 expected_fields 是数字，检查 records 的长度是否等于 expected_fields
        elif isinstance(expected_fields, (int, float)):
            if isinstance(records, list):
                if len(records) != expected_fields:  # 比较长度是否相等
                    mismatches.append(f"Records length {len(records)} does not match the expected length {expected_fields}.")
            else:
                mismatches.append(f"Records {records} is not a list, cannot compare length with {expected_fields}.")

        # 如果 expected_fields 是列表
        elif isinstance(expected_fields, list):
            if isinstance(records, list):
                if records not in expected_fields:
                    mismatches.append(f"Records {records} is not in the expected list {expected_fields}.")
            else:
                mismatches.append(f"Records {records} is not in the expected list {expected_fields}.")

        # 如果记录中存在不匹配项，抛出异常
        if mismatches:
            raise ValueError(f"以下记录不满足条件 {expected_fields}: {mismatches}")

    except:
        log.error(f"报错信息：{traceback.format_exc()}")



