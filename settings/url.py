# coding=utf-8
from handlers import admin_handler, home_handler
from handlers import main_handler,table_test_handler
from handlers.signin_handler import SigninHandler
from handlers.Email import email_smtp_handler,email_exchange_handler
url  =  [                            #
        (r'/', SigninHandler),
        (r'/signin',SigninHandler),
        (r'/main', main_handler.MainHandler),
        (r'/admin/verifyCode',admin_handler.verifyCode),
        (r'/tableTest', table_test_handler.TableTestHandler),
        (r'/sendEmail/stmp',email_smtp_handler.SendEmailHandler),
        (r'/sendEmail/exchange',email_exchange_handler.SendEmailHandler),
        (r'/home',home_handler.HomeHandler),
        ]
