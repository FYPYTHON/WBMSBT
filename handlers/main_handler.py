#coding=utf-8
from handlers.base_handler import BaseHandler
from json import dumps as json_dumps

class MainHandler(BaseHandler):

    def get(self):
        self.render("main.html")


    def post(self):
        self.write(json_dumps({"code:":"1234"}))
        print(self._request_summary())
        # self.redirect('/download')
        return



