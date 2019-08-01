from handlers.base_handler import BaseHandler
from tornado.log import access_log as weblog


class ExtraBaseHandler(BaseHandler):
    def get(self, *args, **kwargs):
        weblog.info("%s. get extrabase.html", self._request_summary())
        return self.render("extrabase.html")    # templates/

    def post(self, *args, **kwargs):
        pass

