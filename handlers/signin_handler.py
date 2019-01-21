#coding=utf-8
import hashlib

from database.tbl_account import TblAccount
from handlers.base_handler import BaseHandler
from json import dumps as json_dumps
import weblog
from message import msg_define
from method.data_encode import MD5


class SigninHandler(BaseHandler):

    def get(self):
        weblog.info("%s ,sign in.",self._request_summary())
        self.render("admin/signin.html")


    def post(self):
        weblog.info("%s ,sign in.", self._request_summary())
        weblog.info("tbl_admin:%s",self.localVariable)
        userAccount = self.get_argument("userAccount")
        password = self.get_argument("password")
        inputCode = self.get_argument("inputCode")

        user = self.mysqldb().query(TblAccount.username,TblAccount.password).first()
        if user is None:
            return self.write(json_dumps({"msg":msg_define.USER_IS_NONE,"error_code":1}))
        if user.username != userAccount or user.password != MD5(password):
            return self.write(json_dumps({"msg":msg_define.USER_OR_PASSWORD_ERROR,"error_code":1}))
        # return self.redirect("/download")
        self.set_secure_cookie("user_account",userAccount)
        # session manager
        # self.session["user_account"] = userAccount
        # self.session.save()
        return self.write(json_dumps({"msg": "", "error_code": 0}))



