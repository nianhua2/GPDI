# Name:         yaml_register.py
# Description:  python作业
# Author:       python23_年华
# Date:         2019/11/2 16:04
import yaml
from futureloan.scripts.handle_path import HandlePath


class HandleYaml:

    def __init__(self, file_name):
        with open(file_name, encoding="UTF-8") as file:
            self.data = yaml.full_load(file)

    # 定义读取yaml文件的方法
    def read_yaml(self, region, option):
        return self.data[region][option]

    # 定义写入yaml文件的方法
    @staticmethod
    def writer_yaml(datas, filename):
        with open(filename, "a+", encoding="utf8")as file:
            # allow_unicode = True 可以写入中文并展示
            yaml.dump(datas, file, allow_unicode=True)


obj_yaml = HandleYaml(HandlePath().get_path("configs", "properties.yaml"))

if __name__ == '__main__':
    obj_yaml = HandleYaml(HandlePath().get_path("configs", "properties.yaml"))

    datas = {
        "excel": {
            "file_name": "cases.xlsx"
        },
        "user": {
            "username": "年华",
            "age": 24,
            "gender": "男"
        }
    }
    ews = obj_yaml.read_yaml("excel","file_name")
    pass