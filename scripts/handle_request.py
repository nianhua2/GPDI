# Name:         futureloan_interface.py
# Description:  python作业
# Author:       python23_年华
# Date:         2019/11/10 13:40
import requests
import json


class HandleRequest:
    def __init__(self):
        # 获得session会话
        self.session = requests.Session()

    def update_headers(self, headers):
        # session中的headers是一个字典，调用update方法更新请求头
        self.session.headers.update(headers)

    # 设置默认的参数，请求方法定位post,默认传参为json格式
    def send_request(self, url, method="post", params=None, is_json=True, **kwargs):
        # 把传入的请求方法变小写
        method = method.lower()
        # 判断请求参数是json格式的字符串还是字典格式的字符串
        if isinstance(params, str):
            # try:
            #     params = json.loads(params)
            # except Exception as e:
            #     params = eval(params)

            # json中含有True/null,调用字符串find方法，找不到返回-1
            if params.find("true") != -1 or params.find("null") != -1 or params.find("false") != -1:
                # json转为字典
                params = json.loads(params)
            elif params.find("Null") != -1:
                print("参数错误，Null应该为null")
            else:
                # 如果是字典格式的字符串直接用eval得到
                params = eval(params)
        else:
            # 不是字符串，本来就是字典格式的，直接传参
            params = params
        if method == 'get':
            # 直接在url后面拼接请求参数
            result = self.session.request(method, url, params=params, **kwargs)
        elif method in ('post', 'put', 'delete', 'patch'):
            if is_json:
                # json格式传参，发起请求
                result = self.session.request(method, url, json=params, **kwargs)
            else:
                # form表单传参，发起请求
                result = self.session.request(method, url, data=params, **kwargs)
        else:
            print(f"请求方法名{method}错误")
            result = None
        return result

    def close(self):
        # 关闭会话
        self.session.close()
