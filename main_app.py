#coding=utf-8

import os.path
import tornado.ioloop
import tornado.web
import tornado.escape
from settings import url
import tornado.options
import warnings
warnings.filterwarnings("ignore")
from handlers.Timeout.timeout_handler import UserOnlineHandler
class Application(tornado.web.Application):
    def __init__(self):

        settings = dict(
            template_path= (os.path.join(os.path.dirname(__file__), "templates")),
            static_path= (os.path.join(os.path.dirname(__file__), "static")),
            cookie_secret="bZJc2sWMakYos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            upload_path=os.path.join(os.path.dirname(__file__), "files"),
            login_url="/signin",
            # debug=False
            # autoescape=None,
        )

        handlers = url.url
        tornado.web.Application.__init__(self, handlers, **settings)

# python -m pip freeze > pip_list.txt
# python -m pip install -r requirements.txt

if __name__ == "__main__":
    app = Application()
    app.listen(8081)
    tornado.options.parse_command_line()
    # tornado.ioloop.PeriodicCallback(UserOnlineHandler.get_online_users,6000).start()
    tornado.ioloop.IOLoop.instance().start()


