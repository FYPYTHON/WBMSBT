# coding=utf-8
from handlers.base_handler import BaseHandler
from handlers.Project.project_manage_handler import get_project_list, get_user_list

class ChartManageHandler(BaseHandler):
    def get(self):
        self.render("project/projectlist.html", projects=get_project_list(self))
        pass

    def post(self):
        pass