#coding=utf-8
import hashlib
from tornado.web import authenticated
from database.tbl_note_list import TblPostList
from handlers.base_handler import BaseHandler
from json import dumps as json_dumps
import weblog


class NoteListHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        notes = self.mysqldb().query(TblPostList).filter_by(status='enabled', type='post').order_by(TblPostList.date.desc()).all()
        return self.render('admin/notelist.html', notes=notes)

    @authenticated
    def post(self):
        pass