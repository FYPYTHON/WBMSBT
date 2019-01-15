#coding=utf-8
import hashlib

from database.tbl_admin import TblAdmin
from handlers.base_handler import BaseHandler
import tornado.web
from json import dumps as json_dumps
import weblog

class TableTestHandler(BaseHandler):

    def get(self):
        weblog.info("%s , TableTestHandler.",self._request_summary())
        data = {"name":"GET","value":"v12","type":1}
        datas = []
        datas.append(data)
        datas.append(data)
        # self.render('tabletest.html',data=datas)
        self.render('project/multiselect.html')

    def post(self):
        print(self.request.uri)
        result = self.mysqldb().query(TblAdmin).all()
        datas = []
        for res in result:
            data = []
            data.append(res.name)
            data.append(res.value)
            data.append(res.type)
            datas.append(data)
        return self.write(json_dumps({"data":datas}))
        # self.redirect("/")


