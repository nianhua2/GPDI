# Name:         my_log.py
# Description:  python作业
# Author:       python23_年华
# Date:         2019/10/30 14:24
import logging

from futureloan.scripts.handle_yaml import obj_yaml
from futureloan.scripts.handle_path import HandlePath


# 自定义一个日志类
class HandleLog:

    @classmethod
    def get_log(cls):
        # 定义一个日志收集器
        my_log = logging.getLogger(obj_yaml.read_yaml("log", "name_collector"))
        # 设置日志收集器的级别
        my_log.setLevel(obj_yaml.read_yaml("log", "level_collector"))

        # 设置日志输出的格式
        formater = logging.Formatter(obj_yaml.read_yaml("log", "formater"))

        # 定义一个日志输出到控制台的输出渠道
        control = logging.StreamHandler()
        # 设置输出渠道的日志级别
        control.setLevel(obj_yaml.read_yaml("log", "level_control"))
        # 添加日志输出的格式
        control.setFormatter(formater)
        # 将输出渠道添加到日志收集器中
        my_log.addHandler(control)

        # 定义一个日志输出到文件的输出渠道
        path = logging.FileHandler(HandlePath().get_path("logs", obj_yaml.read_yaml("log", "name_file")),
                                   encoding="UTF-8")
        # 设置输出渠道的日志级别
        path.setLevel(obj_yaml.read_yaml("log", "level_file"))
        # 添加日志输出的格式
        path.setFormatter(formater)
        # 将输出渠道添加到日志收集器中
        my_log.addHandler(path)
        # 返回log对象
        return my_log


# 创建一个唯一的log对象，避免了在不同模块调用日志模块时，重复执行
log = HandleLog.get_log()
