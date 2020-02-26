# Name:         test_register.py
# Description:  python作业
# Author:       python23_年华
# Date:         2019/10/26 14:16
import unittest

from futureloan.scripts.handle_excel import HandleExcel
from futureloan.libs.ddt import ddt, data
from futureloan.scripts.handle_log import log
from futureloan.scripts.handle_yaml import obj_yaml
from futureloan.scripts.handle_request import HandleRequest
from futureloan.scripts.handle_re import DynamicParameter


@ddt
class LoginTestCase(unittest.TestCase):
    # 定义两个类属性
    read_writer = HandleExcel("login")
    cases = read_writer.read_excel_by_obj()

    @classmethod
    def setUpClass(cls):
        # 创建请求对象
        cls.obj = HandleRequest()
        # 添加请求头
        cls.obj.update_headers(obj_yaml.read_yaml("api", "headers"))

    @classmethod
    def tearDownClass(cls):
        cls.obj.close()

    # ddt会自己遍历cases,每遍历一次，会把对象传给case
    @data(*cases)
    def test_login(self, case):
        # 获取url
        url = obj_yaml.read_yaml("api", "url") + case.url
        # 通过随机生成的手机号来替换Excel文件中的手机号
        new_data = DynamicParameter.dynamic_parameter(case.data)
        # 把字符串格式的字典获取 通过对象.属性名
        expected = eval(case.expected)
        # 发送请求，得到校验后的实际运行结果
        res = self.obj.send_request(url, params=new_data)
        # 转换为json
        result = res.json()
        # 根据excel文件，确定行号与case_id之间的关系
        row = case.case_id + 1
        try:
            # 回写实际结果到actual列,response对象.text转换为文本,这行要写在断言之前，不然断言不过的没办法回写实际结果
            self.read_writer.writer_excel(row=row, column=obj_yaml.read_yaml("msg", "column_actual"), value=res.text)
            # 断言比较code 期望与实际结果
            self.assertEqual(expected["code"], result["code"],case.title)
            # 断言比较msg 期望与实际结果
            self.assertEqual(expected["msg"], result["msg"],case.title)
        except AssertionError as e:
            # 输出日志到文件
            log.error(f"用例： {case.title}   结果：未通过\n具体异常为：{e}\n")
            # 如果异常，回写“未通过”数据到Excel文件
            self.read_writer.writer_excel(row=row, column=obj_yaml.read_yaml("msg", "column"),
                                          value=obj_yaml.read_yaml("msg", "value_fail"))
            # 因为异常被处理，用例执行都是成功（即不会发生断言异常），所以要往外抛出发生的异常
            raise e
        else:
            # 输出日志到文件
            log.info(f"用例： {case.title}   结果：通过")
            # 如果正常，回写“通过”数据到Excel文件
            self.read_writer.writer_excel(row=row, column=obj_yaml.read_yaml("msg", "column"),
                                          value=obj_yaml.read_yaml("msg", "value_pass"))
