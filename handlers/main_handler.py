#coding=utf-8
from tornado.web import authenticated
from handlers.base_handler import BaseHandler
from json import dumps as json_dumps
import weblog


class MainHandler(BaseHandler):
    @authenticated
    def get(self):
        # self.render("testclick.html")
        weblog.info("%s.", self._request_summary())
        self.render("admin/homepage.html")

    @authenticated
    def post(self):

        print(self._request_summary())
        code = self.get_argument("code")
        print(code)
        # self.redirect('/tableTest')
        self.write(json_dumps({"msg":"ok"}))
        return



