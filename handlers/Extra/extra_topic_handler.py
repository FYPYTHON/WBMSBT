# coding=utf-8
# from sqlalchemy import func
from json import dumps as json_dumps
from tornado.web import authenticated
from handlers.base_handler import BaseHandler
from tornado.log import access_log as weblog
from database.tbl_discuss import TblDiscuss
from database.tbl_account import TblAccount
from database.tbl_topic import TblTopic
from handlers.common_handler import PAGESIZE, get_pages, get_user_id, get_topic, get_user_nickname
from tornado import gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor


class TopicAdminHandler(BaseHandler):
    executor = ThreadPoolExecutor(4)

    @run_on_executor
    def get_data(self, current_page):
        uid = get_user_id(self)
        data = self.mysqldb().query(TblTopic.id,
                                    TblTopic.discuss,
                                    TblTopic.likes,
                                    TblAccount.nickname.label("author"),
                                    TblTopic.create,
                                    TblTopic.title,
                                    TblTopic.content,
                                    TblTopic.category)
        data = data.filter(TblTopic.status == 0, TblAccount.id == TblTopic.author)
        data = data.filter(TblTopic.author == uid)
        data = data.limit(PAGESIZE).offset((current_page - 1) * PAGESIZE).all()
        total_count = len(data)
        total_page = get_pages(total_count)
        return data, total_page

    @authenticated
    @gen.coroutine
    def get(self, *args, **kwargs):
        """
        get_user_nickname  and self.current_user
        :param args:
        :param kwargs:
        :return:
        """
        weblog.info("%s. get topicadmin.html", self._request_summary())
        current_page = int(self.get_argument("current_page", "1"))
        topics, total_page = yield self.get_data(current_page)
        self.render("extra/topicadmin.html", topics=topics, user=get_user_nickname(self))  # templates/

    @run_on_executor
    def edit_topic(self, title, content, category, topic_id):

        topic = self.mysqldb().query(TblTopic).filter(TblTopic.id == topic_id).first()
        if topic is None:
            return self.write(json_dumps({"msg": u"该话题不存在，请刷新"}))

        topic.title = title
        topic.content = content
        topic.category = category

        try:
            self.mysqldb().commit()
            return self.write(json_dumps({"msg": None}))
        except Exception as e:
            weblog.error("add topic to mysql error:{}".format(e))
            self.mysqldb().rollback()
            return self.write(json_dumps({"msg": u"修改失败"}))

    @authenticated
    @gen.coroutine
    def put(self):
        weblog.info("%s. put edit a topic", self._request_summary())
        title = self.get_argument("title", None)
        content = self.get_argument("content", None)
        category = int(self.get_argument("category", "0"))
        topic_id = self.get_argument("topic_id", "0")

        if title is None or content is None:
            return self.write(json_dumps({"msg": u"标题或内容不能为空"}))

        yield self.edit_topic(title, content, category, topic_id)


class TopicHandler(BaseHandler):
    executor = ThreadPoolExecutor(4)

    @authenticated
    def get(self, *args, **kwargs):
        weblog.info("%s. get extrabase.html", self._request_summary())
        topic_id = self.get_argument("topic_id", "0")
        topic = get_topic(self, topic_id)
        self.render("extra/topic.html", topic=topic, user=get_user_nickname(self))  # templates/

    @run_on_executor
    def add_topic(self, title, content, category):
        uid = get_user_id(self)
        if uid is None:
            return self.write(json_dumps({"msg": u"您已掉线，请重新登录"}))
        topic = TblTopic()
        topic.title = title
        topic.content = content
        topic.author = uid
        topic.category = category

        try:
            self.mysqldb().add(topic)
            self.mysqldb().commit()
            return self.write(json_dumps({"msg": None}))
        except Exception as e:
            weblog.error("add topic to mysql error:{}".format(e))
            self.mysqldb().rollback()
            return self.write(json_dumps({"msg": u"写入数据库失败"}))

    @authenticated
    @gen.coroutine
    def post(self, *args, **kwargs):
        weblog.info("%s. post add a topic", self._request_summary())
        title = self.get_argument("title", None)
        content = self.get_argument("content", None)
        category = int(self.get_argument("category", "0"))

        if title is None or content is None:
            return self.write(json_dumps({"msg": u"标题或内容不能为空"}))

        yield self.add_topic(title, content, category)



