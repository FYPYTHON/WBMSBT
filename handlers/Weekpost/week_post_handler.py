# coding=utf-8
from tornado.web import authenticated
from tornado.log import access_log as weblog
from handlers.base_handler import BaseHandler


class WeekPostHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        pass

    @authenticated
    def post(self):
        pass