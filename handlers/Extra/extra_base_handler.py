# coding=utf-8
from sqlalchemy import func
from json import dumps as json_dumps
from handlers.base_handler import BaseHandler
from tornado.log import access_log as weblog
from database.tbl_discuss import TblDiscuss
from database.tbl_account import TblAccount
from database.tbl_topic import TblTopic
from handlers.common_handler import PAGESIZE, get_pages
from tornado import gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor


class ExtraBaseHandler(BaseHandler):
    executor = ThreadPoolExecutor(4)

    @run_on_executor
    def get_data(self, current_page):
        data = self.mysqldb().query(TblTopic.id,
                                    TblTopic.discuss,
                                    TblTopic.likes,
                                    TblAccount.nickname.label("author"),
                                    TblTopic.create,
                                    TblTopic.title,
                                    TblTopic.content,
                                    TblTopic.category)
        data = data.filter(TblTopic.status == 0, TblAccount.id == TblTopic.author)
        data = data.limit(PAGESIZE).offset((current_page - 1) * PAGESIZE).all()
        total_count = len(data)
        total_page = get_pages(total_count)
        return data, total_page

    @gen.coroutine
    def get(self, *args, **kwargs):
        weblog.info("%s. get extrabase.html", self._request_summary())
        current_page = int(self.get_argument("current_page", "1"))
        topics, total_page = yield self.get_data(current_page)
        self.render("extrabase.html", topics=topics)    # templates/

    def get_topic(self, current_page, topic_id):
        discount = self.mysqldb().query(func.count('*').label("count"),
                                    TblDiscuss.original.label("id")).group_by(TblDiscuss.original).subquery()
        discuss = self.mysqldb().query(TblDiscuss.id,
                                   TblDiscuss.discuss,
                                   discount.c.count,
                                   TblAccount.nickname.label("author"),
                                   TblDiscuss.topic_id,
                                   TblDiscuss.original,
                                   TblDiscuss.create)
        discuss = discuss.join(discount, discount.c.id == TblDiscuss.id)
        discuss = discuss.filter(TblDiscuss.status == 0, TblDiscuss.author == TblAccount.id,
                                 TblDiscuss.topic_id == topic_id)
        discuss = discuss.order_by(TblDiscuss.create.desc())
        discuss = discuss.limit(PAGESIZE).offset((current_page-1)*PAGESIZE).all()
        total_count = len(discuss)
        total_page = get_pages(total_count)
        return discuss, total_page

    def post(self, *args, **kwargs):
        pass


class DiscussHandler(BaseHandler):
    def get(self, topic_id, *args, **kwargs):
        weblog.info("%s. get discuss.html.topic:%s", self._request_summary(), topic_id)
        current_page = int(self.get_argument("current_page", "1"))
        discuss, totalpage = self.get_discuss(current_page, int(topic_id))
        return self.render("extra/discuss.html", discuss=discuss)

    def get_discuss(self, current_page, topic_id):
        discuss = self.mysqldb().query(TblDiscuss.id,
                                   TblDiscuss.discuss,
                                   TblAccount.nickname.label("author"),
                                   TblDiscuss.topic_id,
                                   TblDiscuss.original,
                                   TblDiscuss.create)
        discuss = discuss.filter(TblDiscuss.status == 0, TblDiscuss.author == TblAccount.id,
                                 TblDiscuss.topic_id == topic_id)
        discuss = discuss.order_by(TblDiscuss.create.desc())
        discuss = discuss.limit(PAGESIZE).offset((current_page-1)*PAGESIZE).all()
        total_count = len(discuss)
        total_page = get_pages(total_count)
        return discuss, total_page

    def post(self, topic_id, *args, **kwargs):
        dicuess = self.get_argument("discuss")
        did = self.get_argument("did", '0')
        # topic_id = self.get_argument("topic_id", None)

        if dicuess is None or dicuess == "":
            msg = u"评论不能为空"
            return self.write(json_dumps({"msg": msg}))
        if did is None or topic_id is None:
            msg = u"获取信息失败"
            return self.write(json_dumps({"msg": msg}))
        else:
            topic_id = int(topic_id)
            did = int(did)

        user_id = self.mysqldb().query(TblAccount.id).filter(TblAccount.username == self.current_user).first()
        if user_id is None:
            uid = 1
        else:
            uid = user_id[0]
        new_discuss = TblDiscuss()
        new_discuss.status = 0
        new_discuss.discuss = dicuess
        new_discuss.original = did
        new_discuss.topic_id = topic_id
        new_discuss.author = uid
        topic = self.mysqldb().query(TblTopic).filter(TblTopic.id == topic_id).first()
        topic.discuss += 1
        print(self.current_user, topic.discuss)
        try:
            self.mysqldb().add(new_discuss)
            self.mysqldb().commit()
            return self.write(json_dumps({"msg": None}))
        except Exception as e:
            self.mysqldb().rollback()
            msg = u"发布失败"
            weblog.error("publish dicuess error:{}".format(e))
            return self.write(json_dumps({"msg": msg}))

