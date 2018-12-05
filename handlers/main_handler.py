#coding=utf-8
from handlers.base_handler import BaseHandler
from json import dumps as json_dumps

class MainHandler(BaseHandler):

    def get(self):
        # self.render("testclick.html")
        self.render("admin/homepage.html")


    def post(self):

        print(self._request_summary())
        code = self.get_argument("code")
        print(code)
        # self.redirect('/tableTest')
        self.write(json_dumps({"msg":"ok"}))
        return



