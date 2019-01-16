# coding=utf-8
from handlers.base_handler import BaseHandler
from handlers.Project.project_manage_handler import get_project_list, get_user_list

class TaskManageHandler(BaseHandler):
    def get(self):
        self.render("project/task.html", message="", projects=get_project_list(self), users=get_user_list(self))
        pass

    def post(self):
        pass