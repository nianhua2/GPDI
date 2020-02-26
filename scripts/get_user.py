# Name:         run_get_user.py
# Description:  python作业
# Author:       python23_年华
# Date:         2019/11/17 21:26
from futureloan.scripts.handle_yaml import HandleYaml, obj_yaml
from futureloan.scripts.handle_path import HandlePath
from futureloan.scripts.handle_request import HandleRequest
from futureloan.scripts.handle_mysql import HandleMysql


class CreateUserRoles:

    @staticmethod
    def create_user_roles(region, reg_name, type=1):
        url = "http://api.lemonban.com/futureloan/member/register"
        # 创建mysql对象
        obj_mysql = HandleMysql()
        # 创建请求对象
        obj = HandleRequest()
        # 添加请求头
        obj.update_headers(obj_yaml.read_yaml("register", "headers"))
        # 得到未注册的手机号
        phone = obj_mysql.create_new_mobilephone()
        params = {"mobile_phone": phone, "pwd": "12345678", "type": type, "reg_name": reg_name}
        # 发送请求，
        user = obj.send_request(url, params=params).json()
        data = {
            region: {
                "id": user['data']['id'],
                "reg_name": reg_name,
                "mobile_phone": phone,
                "pwd": "12345678",
                "type": type,
                "leave_amount": 0
            }
        }

        HandleYaml.writer_yaml(data, HandlePath().get_path("configs", "user.yaml"))
        obj.close()
        obj_mysql.close()


if __name__ == '__main__':
    CreateUserRoles.create_user_roles("borrower", "借款人")
    CreateUserRoles.create_user_roles("investor", "投资人")
    CreateUserRoles.create_user_roles("admin", "管理人", type=0)
