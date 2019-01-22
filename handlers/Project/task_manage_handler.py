# coding=utf-8
from tornado.web import authenticated
from handlers.base_handler import BaseHandler
import weblog
from handlers.Project.project_manage_handler import get_project_list, get_user_list


class TaskManageHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        task = dict()
        task['progress'] = 45
        self.render("project/task.html", message="", projects=get_project_list(self),
                    users=get_user_list(self), task=task)
        pass

    @authenticated
    def post(self):
        pass