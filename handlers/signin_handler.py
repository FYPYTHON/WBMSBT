#coding=utf-8
import hashlib

from database.tbl_account import TblAccount
from handlers.base_handler import BaseHandler
from json import dumps as json_dumps
from tornado.log import access_log as weblog
from message import msg_define
from method.data_encode import MD5, generate_uuid
SESSION_ID = msg_define.SESSION_ID

class LogoutHandler(BaseHandler):
    def get(self):
        weblog.info("%s ,logout", self._request_summary())
        self.clear_cookie(SESSION_ID)
        self.redis.delete(SESSION_ID)
        self.redirect('/signin')


class SigninHandler(BaseHandler):

    def get(self):
        weblog.info("%s ,sign in.",self._request_summary())
        self.render("admin/signin.html")


    def post(self):
        weblog.info("%s ,sign in.", self._request_summary())
        # weblog.info("tbl_admin:%s", self.localVariable)
        userAccount = self.get_argument("userAccount")
        password = self.get_argument("password")
        inputCode = self.get_argument("inputCode")

        user = self.mysqldb().query(TblAccount.username, TblAccount.password).filter_by(username=userAccount).first()
        if user is None:
            return self.write(json_dumps({"msg": msg_define.USER_IS_NONE, "error_code": 1}))
        if user.username != userAccount or user.password != MD5(password):
            weblog.error("user password input:{}, ori:{}".format(user.password, MD5(password)))
            return self.write(json_dumps({"msg": msg_define.USER_OR_PASSWORD_ERROR, "error_code": 1}))
        if inputCode.upper() != self.get_secure_cookie("code").decode('utf-8').upper():
            weblog.error("code you inut:{}, ori code:{}".format(inputCode.upper(),
                        self.get_secure_cookie("code").decode('utf-8').upper()))
            return self.write(json_dumps({"msg": msg_define.VER_CODE_ERROR, "error_code": 1}))
        # return self.redirect("/download")
        # self.set_secure_cookie("user_account", userAccount)
        session_id = generate_uuid()
        self.set_secure_cookie(SESSION_ID, session_id)
        # print("timeout:", self.application.settings['session_timeout'])
        self.redis.set(session_id, userAccount, self.application.settings['session_timeout'])
        # session manager
        # self.session["user_account"] = userAccount
        # self.session.save()
        # weblog.info(self.session.get('user_account'))
        # weblog.info(self.session.get(self))
        return self.write(json_dumps({"msg": "", "error_code": 0}))
        # return self.redirect('/home')




