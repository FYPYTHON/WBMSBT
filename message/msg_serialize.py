# coding=utf-8
import json
from message import data_type, class_serializable


class UserInfo(class_serializable.JsonSerializableObj):
    __ATTR_DEF__ = {
          "id": data_type.MY_INT16
        , "username": data_type.MY_STRING
        , "password": data_type.MY_STRING
        , "email": data_type.MY_STRING
        , "userstate": data_type.MY_INT16
        , "userrole": data_type.MY_INT16
        , "register_time": data_type.MY_STRING
        , "avatar_path": data_type.MY_STRING
    }

    def __init__(self):
        self.init_all_attr()


class PageInfoList(class_serializable.JsonSerializableObj):
    __ATTR_DEF__ = {
          "datalist": [UserInfo]
        , "current_page": data_type.MY_INT16
        , "total_page": data_type.MY_INT16
        , "page_size" : data_type.MY_INT16
    }

    def __init__(self):
        self.init_all_attr()
        self.datalist = []


class RespMessage(class_serializable.JsonSerializableObj):
    __ATTR_DEF__ = {
          "rep_msg": data_type.MY_STRING
        , "err_code": data_type.MY_STRING
    }


