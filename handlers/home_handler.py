# coding=utf-8
import weblog
from handlers.base_handler import BaseHandler


class HomeHandler(BaseHandler):
    def get(self):
        weblog.info("%s , get home(base) html.",self._request_summary())
        self.render("base.html")