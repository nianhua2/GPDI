# Name:         handle_path.py
# Description:  python作业
# Author:       python23_年华
# Date:         2019/11/17 15:35
import os


class HandlePath:

    def __init__(self):
        # 实际上也是退两层，写的太繁琐，舍弃
        self.BASE_DIR =  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # 推荐直接用abspath(".").如果有多层，用../..
        # self.BASE_DIR = os.path.abspath(".")

    def get_path(self, dir_name, file_name=None):
        if file_name is None:
            # 不传文件名，则返回目录的路径
            return os.path.join(self.BASE_DIR, dir_name)
        else:
            # 传文件名，返回文件的路径
            return os.path.join(os.path.join(self.BASE_DIR, dir_name), file_name)


if __name__ == '__main__':
    print(HandlePath().get_path('configs'))
    print(HandlePath().get_path('configs', 'properties.yaml'))
