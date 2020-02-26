# Name:         handle_mysql.py
# Description:  python作业
# Author:       python23_年华
# Date:         2019/11/14 20:40
import pymysql
import random

from futureloan.scripts.handle_yaml import obj_yaml


class HandleMysql:

    def __init__(self):
        self.conn = pymysql.connect(host=obj_yaml.read_yaml("mysql", "host"),
                                    user=obj_yaml.read_yaml("mysql", "user"),
                                    password=obj_yaml.read_yaml("mysql", "password"),
                                    db=obj_yaml.read_yaml("mysql", "db"),
                                    charset='utf8',
                                    cursorclass=pymysql.cursors.DictCursor
                                    )
        self.cursor = self.conn.cursor()

    def select_sql(self, sql, args=None, is_more=False):
        # type args: tuple, list or dict
        self.cursor.execute(sql, args)
        self.conn.commit()
        if is_more:
            return self.cursor.fetchall()
        else:
            return self.cursor.fetchone()

    def close(self):
        self.cursor.close()
        self.conn.close()

    # 得到一个号段+随机8位数的手机号
    @staticmethod
    def create_mobilephone():
        return '138' + ''.join(random.sample('0123456789', 8))

    def judge_mobile_exist(self, mobilephone):
        sql = obj_yaml.read_yaml("mysql","select_member")
        # args传值类型type args: tuple, list or dict(源码）
        # 如果在数据库中能查到，说明不为空，返回True
        if self.select_sql(sql, args=[mobilephone]):
            return True
        else:
            return False

    def create_new_mobilephone(self):
        while True:
            mobilephone = self.create_mobilephone()
            if not self.judge_mobile_exist(mobilephone):
                break
        return mobilephone




if __name__ == '__main__':
    # sql = "select * from member t where t.mobile_phone= '13888888811';"
    # sql = "select * from member t where t.mobile_phone= %s;"
    # obj = HandleMysql().select_sql(sql,args=['13888888811'])
    # obj = HandleMysql().select_sql(sql)
    obj = HandleMysql().create_new_mobilephone()
    print(obj)
