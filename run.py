# Name:         run_register.py
# Description:  python作业
# Author:       python23_年华
# Date:         2019/10/26 14:52
import unittest
import os
from datetime import datetime

from libs.HTMLTestRunnerNew import HTMLTestRunner
from scripts.handle_yaml import obj_yaml
from scripts.handle_path import HandlePath
from scripts.get_user import CreateUserRoles

# 得到时间戳
time = datetime.now().strftime('%Y%m%d%H%M%S')

# 创建测试套件
# suite = unittest.TestSuite()
# 创建加载测试用例容器
# loader = unittest.TestLoader()
# 加载注册接口用例到套件
# suite.addTest(loader.loadTestsFromModule(test_01_register))
# 使用discover来加载用例模块
# 第一个参数为查询用例模块所在的目录路径, 第二个参数为通配符(参考模糊查询)
suite = unittest.defaultTestLoader.discover(HandlePath().get_path("cases"))
# 创建测试运行程序
runner = HTMLTestRunner(
    stream=open(HandlePath().get_path("reports", obj_yaml.read_yaml("html", "html_report") + time + ".html"), "wb"),
    title=obj_yaml.read_yaml("html", "title"),
    description=obj_yaml.read_yaml("html", "description"),
    tester=obj_yaml.read_yaml("html", "tester"))

# 判断文件是否已存在，若不存在则创建三个账号  存在则不用创建
if not os.path.exists(HandlePath().get_path("configs", "user.yaml")):
    CreateUserRoles.create_user_roles("borrower", "借款人")
    CreateUserRoles.create_user_roles("investor", "投资人")
    CreateUserRoles.create_user_roles("admin", "管理人", type=0)
# 执行套件用的测试用例
runner.run(suite)
