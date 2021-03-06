#coding=utf-8
from tornado.web import authenticated
from handlers.base_handler import BaseHandler
from json import dumps as json_dumps
# from tornado.log import access_log as weblog
from tornado.log import access_log as weblog
from tornado import gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
import os
from datetime import datetime

class MainHandler(BaseHandler):
    executor = ThreadPoolExecutor(4)
    # @authenticated

    # @gen.coroutine
    @run_on_executor
    def doing(self):
        import time
        # time.sleep(10)
        return str(datetime.now())

    @gen.coroutine
    def get(self):
        print(datetime.now(), "start")
        # self.render("testclick.html")
        weblog.info("%s.", self._request_summary())
        weblog.info("get home")
        result = yield self.doing()
        print(result)
        # self.render("admin/homepage.html")
        self.write(self.render_template('admin/homepage.html'))
        # return self.write("ok," + result)

    @authenticated
    def post(self):

        print(self._request_summary())
        code = self.get_argument("code")
        print(code)
        # self.redirect('/tableTest')
        self.write(json_dumps({"msg": "ok"}))
        return



