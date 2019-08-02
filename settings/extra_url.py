# coding=utf-8
from handlers.Extra.extra_base_handler import ExtraBaseHandler, DiscussHandler
extra_url = [
    (r'/extra', ExtraBaseHandler),
    (r'/discuss/([0-9]+)', DiscussHandler),
]
