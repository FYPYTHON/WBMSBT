#coding=utf-8
import hashlib
from handlers.base_handler import BaseHandler
from json import dumps as json_dumps
import weblog

class SigninHandler(BaseHandler):

    def get(self):

        print("tbl_admin:",self.localVariable)
        weblog.info("%s ,sign in.",self._request_summary())
        self.render("admin/signin.html")


    def post(self):
        weblog.info("%s ,sign in.", self._request_summary())

        userAccount = self.get_argument("userAccount")
        password = self.get_argument("password")
        inputCode = self.get_argument("inputCode")

        # return self.redirect("/download")
        return self.write(json_dumps({"msg":"ok","error_code":0}))



