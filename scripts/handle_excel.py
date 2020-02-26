# Name:         read_writer_excel.py
# Description:  python作业
# Author:       python23_年华
# Date:         2019/10/26 13:36
import openpyxl

from futureloan.scripts.handle_path import HandlePath
from futureloan.scripts.handle_yaml import obj_yaml


# 定义了一类，方便创建对象，通过setattr方法设置对象属性、属性值
class DataClass:
    pass


# 定义一个 读、写 Excel文件的类
class HandleExcel:
    # 文件名、工作簿名 实例化
    def __init__(self, sheet_name, file_name=None):
        if file_name is None:
            # 不传文件名，默认读取datas目录下的文件
            self.file_name = HandlePath().get_path("datas", obj_yaml.read_yaml("excel", "file_name"))
        else:
            self.file_name = file_name
        self.sheet_name = sheet_name

    # 打开文件、工作簿
    def open(self):
        self.work_book = openpyxl.load_workbook(self.file_name)
        self.sheet = self.work_book[self.sheet_name]

    # 读Excel  通过对象存储在列表的方式
    def read_excel_by_obj(self):
        self.open()
        rows = list(self.sheet.rows)
        # 定义了一列表，用来存放测试用例对象
        # 最后返回的这个列表要写到类里面，写在类外面类管理不到
        cases = []
        # 把Excel中的第一行表头数据 抽取出来存在一个列表里
        list_header = [header.value for header in rows[0]]

        # 获取除表头外的其他行数据
        for row in rows[1:]:
            # 每一行的数据加到一个列表里
            list_content = [content.value for content in row]
            # 创建一个对象
            obj = DataClass()
            # 表头和其他行 聚合打包后存储在一个zip对象里  遍历这个对象
            for i in zip(list_header, list_content):
                # 设置对象属性、属性值
                setattr(obj, i[0], i[1])
            # 把所有的对象加入到大列表里
            cases.append(obj)
        # 关闭文档
        self.work_book.close()
        return cases

    # 写数据到Excel
    def writer_excel(self, row, column, value):
        self.open()
        # 通过cell方法，指定写入位置，写入数据
        self.sheet.cell(row=row, column=column, value=value)
        # 保存文件
        self.work_book.save(self.file_name)
        self.work_book.close()


if __name__ == '__main__':
    read_writer = HandleExcel('register')
    print(read_writer.read_excel_by_obj())
