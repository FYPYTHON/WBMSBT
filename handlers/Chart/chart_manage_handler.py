# coding=utf-8
from tornado.web import authenticated
from handlers.base_handler import BaseHandler
from handlers.Project.project_manage_handler import get_project_list, get_user_list


class ChartManageHandler(BaseHandler):
    @authenticated
    def get(self):
        self.render("project/projectlist.html", projects=get_project_list(self))
        pass

    @authenticated
    def post(self):
        pass