#coding=utf-8
import hashlib

from handlers.base_handler import BaseHandler
from json import dumps as json_dumps
import weblog


class UserSettingHandler(BaseHandler):

    def get(self):
        weblog.info("%s , get usersetting html.", self._request_summary())
        setting = {}
        setting['blogname'] = "feiying"
        setting['blogdescription'] = "test only"
        setting['admin_email'] = "xx@qq.com"
        setting['users_can_register'] = "1"
        setting['users_can_comment'] = "1"
        setting['comments_notify'] = "1"
        setting['default_category'] = "default category"
        setting['posts_per_page'] = 10
        setting['posts_per_rss'] = 10
        setting['rss_use_excerpt'] = "1"
        self.render("admin/usersetting.html",setting = setting,success=False)