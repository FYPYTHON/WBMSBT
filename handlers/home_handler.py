# coding=utf-8
from tornado.web import authenticated
import weblog
from handlers.base_handler import BaseHandler


class HomeHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s , get home(base) html.",self._request_summary())
        self.render("base.html")