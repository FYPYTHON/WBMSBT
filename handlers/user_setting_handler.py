#coding=utf-8
import hashlib
from tornado.web import authenticated
from database.tbl_admin import TblAdmin
from handlers.base_handler import BaseHandler
from json import dumps as json_dumps
from tornado.log import access_log as weblog


class UserSettingHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s , get usersetting html.", self._request_summary())
        self.render("admin/usersetting.html",setting = self.get_setting(),success=False)

    def get_setting(self):

        option_list = self.mysqldb().query(TblAdmin).all()
        option_dict = {option.name: option.value for option in option_list}
        return option_dict