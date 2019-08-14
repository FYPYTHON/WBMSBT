# coding=utf-8
# from sqlalchemy import func
from json import dumps as json_dumps
from tornado.web import authenticated
from handlers.base_handler import BaseHandler
from tornado.log import access_log as weblog
from database.tbl_discuss import TblDiscuss
from database.tbl_account import TblAccount
from database.tbl_topic import TblTopic
from handlers.common_handler import PAGESIZE, get_pages, get_user_id, get_topic, get_user_nickname
from tornado import gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor


class ExtraSettingHandler(BaseHandler):
    executor = ThreadPoolExecutor(4)

    @run_on_executor
    def get_data(self):
        data_dict = dict()
        # localV = self.localVariable
        data_dict["localv"] = self.localVariable
        data_dict["localr"] = dict()
        for key in self.redis.keys():
            if len(key) < 20:
                data_dict["localr"][key] = self.redis.get(key)
        data_dict["localr"]["current_user"] = self.redis.get(self.get_secure_cookie("session_id"))
        import time
        time.sleep(10 * 60)
        return data_dict

    @authenticated
    @gen.coroutine
    def get(self, *args, **kwargs):
        weblog.info("%s.", self._request_summary())
        data = yield self.get_data()
        # print(data)
        self.render("extra/setting.html", user=get_user_nickname(self), data=data)
        pass

    def post(self, *args, **kwargs):
        pass
