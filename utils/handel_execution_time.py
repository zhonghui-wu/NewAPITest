# 用于计算用例执行时间的装饰器
import time


def execution_time(func):
    def inner(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f'执行耗时：{end_time-start_time}s')
        return result
    return inner