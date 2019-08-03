# coding=utf-8
from database.tbl_account import TblAccount
from database.tbl_topic import TblTopic
PAGESIZE = 5
FIRST_PAGE = 1


def get_pages(total_page):
    pages = total_page // PAGESIZE + 1
    return pages


def get_user_id(self):
    user_id = self.mysqldb().query(TblAccount.id, TblAccount.nickname).filter(
        TblAccount.username == self.current_user).first()
    if user_id is None:
        uid = None
    else:
        uid = user_id.id
    return uid


def get_topic(self, topic_id):
    topic = self.mysqldb().query(TblTopic.id, TblTopic.category,
                                   TblTopic.title, TblTopic.content).filter(
        TblTopic.id == topic_id).first()
    if topic is None:
        return None
    else:
        return topic