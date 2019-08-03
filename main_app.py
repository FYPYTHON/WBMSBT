#coding=utf-8
import sys
import os.path
# import tornado.httpserver
# import tornado.wsgi
import tornado.ioloop
import tornado.web
import tornado.escape
from settings import url
from method.session import redis_session
import tornado.options
import logging.config
from settings.logconfig import logconfig
# from tornado.log import access_log as weblog
import warnings
warnings.filterwarnings("ignore")
from handlers.Timeout.timeout_handler import UserOnlineHandler
from tornado.options import define, options

define("port", default=8081, help="run on the given port", type=int)
logging.config.dictConfig(logconfig)


class Application(tornado.web.Application):
    def __init__(self):

        settings = dict(
            template_path=(os.path.join(os.path.dirname(__file__), "templates")),
            static_path=(os.path.join(os.path.dirname(__file__), "static")),
            cookie_secret="bZJc2sWMakYos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            session_secret="bZJc2sWMakYos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            session_timeout=600,
            upload_path=os.path.join(os.path.dirname(__file__), "files"),
            login_url="/signin",
            store_options={
                'redis_host': 'localhost',
                'redis_port': 6379,
                'redis_pass': 'feiying'
            }
            # debug=False
            # autoescape=None,
        )

        handlers = url.url
        tornado.web.Application.__init__(self, handlers, **settings)
        self.session_manager = redis_session.SessionManager(settings["session_secret"],
                                                            settings["store_options"],
                                                            settings["session_timeout"])


# python -m pip freeze > pip_list.txt
# python -m pip install -r requirements.txt


if __name__ == "__main__":
    tornado.options.parse_command_line()
    # print(options.port)
    # print(sys.argv[1])
    app = Application()
    # http_server = tornado.httpserver.HTTPServer(app)
    # http_server.listen(options.port)
    app.listen(options.port)

    # tornado.ioloop.PeriodicCallback(UserOnlineHandler.get_online_users,6000).start()

    tornado.ioloop.IOLoop.instance().start()



