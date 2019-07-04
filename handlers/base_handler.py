# coding=utf-8
import datetime
import tornado.web
import tornado.options
from tornado.web import authenticated
import weblog
from database.db_config import db_session
from database.tbl_admin import TblAdmin
from message.msg_define import SESSION_ID
from method.session import redis_session
import redis

class BaseHandler(tornado.web.RequestHandler):
    localStore = {}

    def __init__(self, *argc, **argkw):
        # print("init...")
        # self.session = None
        self.redis = redis.StrictRedis(host='localhost', port=6379, password='feiying')
        super(BaseHandler, self).__init__(*argc, **argkw)
        # self.session = redis_session.Session(self.application.session_manager, self)
        pass

    def initialize(self):
        pass

    # def __init__(self, *argc, **argkw):
        """
        定义 handler 的 session, 注意，根据 HTTP 特点.
        每次访问都会初始化一个 Session 实例哦，这对于你后面的理解很重要
        """
        # self.session = redis_session.Session(self.application.session_manager, self)
        # print("initalize...", self.session)
        self.localVariable = {}
        self.initLocalVariable()
        self.browsing_history()
        # super(BaseHandler, self).__init__(*argc, **argkw)

    # @authenticated
    def get(self, *args, **kwargs):
        pass

    # @authenticated
    def post(self, *args, **kwargs):
        pass

    def mysqldb(self):
        return db_session

    def on_finish(self):
        self.mysqldb().close()

    def get_current_user(self):

        if self.request.uri.startswith(self.get_login_url()) or self.request.uri.startswith('/admin/verifyCode'):
            return "ok"
        session_id = self.get_secure_cookie(SESSION_ID)
        if session_id is None:
            return None
        else:
            session_id = session_id.decode('utf-8')
        user = self.redis.get(session_id)
        if user is None:
            return None
        else:
            return user

        # print(self.request.method, self.request.uri)
        # if self.request.uri.startswith("/signin") or self.request.uri.startswith('/admin/verifyCode'):
        #     return False
        # else:
        #     # print("get_current_user 2:", self.session.get("user_account"))
        #     return self.session.get("user_account")  # redis session



        # if self.get_secure_cookie("user_account") is not None:
        #     return self.get_secure_cookie("user_account")
        # else:
        #     return None

    def initLocalVariable(self):
        variables = self.mysqldb().query(TblAdmin).all()
        for var in variables:
            if var.name not in self.localVariable.keys():
                self.localVariable[var.name] = var.value

    def browsing_history(self):
        login_name = self.get_current_user()
        if login_name is None:
            return
        if type(login_name) == bytes:
            login_name = bytes.decode(login_name)
        try:
            self.mysqldb().execute(
                "INSERT INTO tbl_browsing_history (user_ip,user_account,request_method,"
                "uri,status,browsing_date,browsing_time,user_agent) "
                "VALUES(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');"
                %(self.request.remote_ip, login_name, self.request.uri,self.request.method,
                  self.get_status(),datetime.datetime.now().strftime('%Y%m%d'),
                  datetime.datetime.now().strftime('%H%M%S'), self.request.headers.get("User-Agent"))
            )
            self.mysqldb().commit()
        except:
            weblog.exception("BaseHandler:visit_history error")
            self.mysqldb().rollback()

