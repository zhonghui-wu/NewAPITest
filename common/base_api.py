# -*- coding: utf-8 -*-
# @File: base_api.py
# @Time: 2025/7/21 10:45
# @Author: rock
# @Email: 1187338689@qq.com
import inspect
import requests
from utils.handle_yaml import get_yaml_data
from utils.handle_path import api_config_yaml_path
from configs.config import HOST
from configs.config import LOGIN_HEADER
from utils.logger import log
import traceback  # 最全的报错日志信息



class BaseAPI:

    def __init__(self, token=None, **kwargs): # 初始化--每一个子类都会执行这段代码
        if token:
            self.header = {'Blade-Auth': token}
            self.header.update(kwargs) # 可能其他接口有的需要传多个参数，做拓展
        else:
            self.header = LOGIN_HEADER
        # 用于读取调用子类的名称来拿对应api_config.yaml文件中的接口信息
        self.api_data = get_yaml_data(api_config_yaml_path)[self.__class__.__name__]
        # print(self.api_data)
        # print("这个self实例是：", self.__class__.__name__)

    def request_send(self, **kwargs): # 公共发送方法
        try:
            # 每一个接口都需要读取yaml中对应的接口信息
            # print("谁调用了我：", inspect.stack()[1][3])    inspect.stack()[1][3]等于类名，如：test_login
            self._config_data = self.api_data[inspect.stack()[1][3]]
            # print(self._config_data)
            resp = requests.request(self._config_data['method'],f"{HOST}{self._config_data['path']}",
                                    headers = self.header, **kwargs)

            # ------------------------打印请求详情信息------------------------
            log.info(f"""业务:{self.__class__.__name__},接口:{inspect.stack()[1][3]},
            请求体:{kwargs},
            请求URL:{resp.request.url},
            响应数据:{resp.json()}

            
            """)
            # ------------------------打印请求详情信息------------------------
            return resp.json()

        except:
            log.error(f"报错信息：{traceback.format_exc()}")


    def list(self, **kwargs):
        return self.request_send(**kwargs)

    def submit(self, **kwargs): # 创建/编辑都用这一个
        return self.request_send(**kwargs)

    def delete(self, **kwargs):
        return self.request_send(**kwargs)

    def enable(self, **kwargs): # 启用禁用供方都用这一个
        return self.request_send(**kwargs)




if __name__ == '__main__':
    pass

