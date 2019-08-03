# coding=utf-8
from handlers.Extra.extra_base_handler import ExtraBaseHandler, DiscussHandler
from handlers.Extra.extra_topic_handler import TopicHandler, TopicAdminHandler
extra_url = [
    (r'/extra', ExtraBaseHandler),
    (r'/discuss/([0-9]+)', DiscussHandler),
    (r'/topic', TopicHandler),
    (r'/topic/admin', TopicAdminHandler),
]
