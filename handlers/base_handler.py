#coding=utf-8
import tornado.web
import tornado.options
from database.db_config import db_session
from database.t_admin import TAdmin
class BaseHandler(tornado.web.RequestHandler):
    localStore = {}

    def __init__(self, *argc, **argkw):
        """
        定义 handler 的 session, 注意，根据 HTTP 特点.
        每次访问都会初始化一个 Session 实例哦，这对于你后面的理解很重要
        """
        self.localVariable = {}
        self.initLocalVariable()
        super(BaseHandler, self).__init__(*argc, **argkw)

    def mysqldb(self):
        return db_session

    def on_finish(self):
        self.mysqldb().close()

    # def get_current_user(self):
    #     return self.get_secure_cookie("loginName")

    def initLocalVariable(self):
        variables = self.mysqldb().query(TAdmin).all()
        for var in variables:
            if var.name not in self.localVariable.keys():
                self.localVariable[var.name] = var.value
