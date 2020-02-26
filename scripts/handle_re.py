# Name:         handle_re.py
# Description:  python作业
# Author:       python23_年华
# Date:         2019/11/17 18:08
import re
from futureloan.scripts.handle_mysql import HandleMysql
from futureloan.scripts.handle_yaml import HandleYaml
from futureloan.scripts.handle_path import HandlePath


class DynamicParameter:
    not_existed_tel = r'{not_existed_tel}'

    not_user_id = r'{not_user_id}'

    not_existed_loan_id = '{not_existed_loan_id}'

    borrower_existed_tel = r'{borrower_existed_tel}'

    borrow_user_id = '{borrow_user_id}'

    invest_user_tel = r'{invest_user_tel}'

    invest_user_id = r'{invest_user_id}'

    admin_user_tel = r'{admin_user_tel}'

    loan_id_param = '{loan_id}'

    @classmethod
    def dynamic_not_parms(cls, data):
        # 创建对象
        obj_mysql = HandleMysql()
        # 不存在手机号替换
        if cls.not_existed_tel in data:
            # 手机号替换正则表达式中的表达式
            data = re.sub(cls.not_existed_tel, obj_mysql.create_new_mobilephone(), data)

        # 不存在用户id
        if cls.not_user_id in data:
            obj_yaml = HandleYaml(HandlePath().get_path("configs", "properties.yaml"))
            # 得到不存在的id
            new_user_id = obj_mysql.select_sql(obj_yaml.read_yaml("mysql", "select_max_member_id"))['max(id)'] + 1
            # 手机号替换正则表达式中的表达式,str转为字符串
            data = re.sub(cls.not_user_id, str(new_user_id), data)

        # 不存在loanId
        if cls.not_existed_loan_id in data:
            obj_yaml = HandleYaml(HandlePath().get_path("configs", "properties.yaml"))
            # 得到不存在的id
            new_loan_id = obj_mysql.select_sql(obj_yaml.read_yaml("mysql", "select_max_loan_id"))['max(id)'] + 1
            # 手机号替换正则表达式中的表达式,str转为字符串
            data = re.sub(cls.not_existed_loan_id, str(new_loan_id), data)
        # 关闭对象
        obj_mysql.close()
        return data

    @classmethod
    def dynamic_borrower(cls, data):
        # 借款人手机号
        if cls.borrower_existed_tel in data:
            obj_yaml = HandleYaml(HandlePath().get_path("configs", "user.yaml"))
            # 手机号替换正则表达式中的表达式
            data = re.sub(cls.borrower_existed_tel, obj_yaml.read_yaml("borrower", "mobile_phone"), data)

        # 借款人Id
        if cls.borrow_user_id in data:
            obj_yaml = HandleYaml(HandlePath().get_path("configs", "user.yaml"))
            # 手机号替换正则表达式中的表达式,str转为字符串
            data = re.sub(cls.borrow_user_id, str(obj_yaml.read_yaml("borrower", "id")), data)
        return data

    @classmethod
    def dynamic_invest(cls, data):
        # 投资人手机号
        if cls.invest_user_tel in data:
            obj_yaml = HandleYaml(HandlePath().get_path("configs", "user.yaml"))
            # 手机号替换正则表达式中的表达式
            data = re.sub(cls.invest_user_tel, obj_yaml.read_yaml("investor", "mobile_phone"), data)

        # 投资人ID
        if cls.invest_user_id in data:
            obj_yaml = HandleYaml(HandlePath().get_path("configs", "user.yaml"))
            # 手机号替换正则表达式中的表达式,str转为字符串
            data = re.sub(cls.invest_user_id, str(obj_yaml.read_yaml("investor", "id")), data)
        return data

    @classmethod
    def dynamic_admin(cls, data):
        if cls.admin_user_tel in data:
            obj_yaml = HandleYaml(HandlePath().get_path("configs", "user.yaml"))
            # 手机号替换正则表达式中的表达式
            data = re.sub(cls.admin_user_tel, obj_yaml.read_yaml("admin", "mobile_phone"), data)
        return data

    @classmethod
    def dynamic_interface_relation(cls, data):
        # loanId作接口之间的关联
        if cls.loan_id_param in data:
            # 通过getattr从DynamicParameter中获取loan_id这个属性的值
            data = re.sub(cls.loan_id_param, str(getattr(cls, 'loan_id')), data)
        return data

    @classmethod
    def dynamic_parameter(cls, data):
        data = cls.dynamic_not_parms(data)
        data = cls.dynamic_borrower(data)
        data = cls.dynamic_invest(data)
        data = cls.dynamic_admin(data)
        data = cls.dynamic_interface_relation(data)
        return data


if __name__ == '__main__':
    one_str = '{"mobile_phone": "{not_existed_tel}", "pwd": "12345678", "type": 1, "reg_name": "KeYou"}'
    one_str_1 = '{"mobile_phone": "{borrower_existed_tel}", "pwd": "12345678"}'
    one_str_2 = '{"member_id":{not_user_id},"amount":620}'
    one_str_3 = '{"member_id":{invest_user_id},"amount":500}'
    one_str_4 = 'SELECT leave_amount FROM member WHERE id = {invest_user_id};'
    one_str_5 = '{"mobile_phone": {invest_user_tel},"pwd":"12345678"}'

    one_str_6 = '{"member_id":{borrow_user_id},"title":"借钱实现财富自由","amount":2000,"loan_rate":12.0,"loan_term":3,"loan_date_type":1,"bidding_days":5}'
    one_str_7 = '{"mobile_phone":"{admin_user_tel}","pwd":"12345678"}'
    one_str_8 = '{"member_id":{invest_user_id}, "loan_id":{not_existed_loan_id},"amount":300}'
    res = DynamicParameter.dynamic_parameter(one_str_1)
    pass
