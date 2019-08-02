# coding=utf-8

from sqlalchemy import Column, String, Integer,DateTime, Text
from datetime import datetime
from database import table_base
from database.db_config import ModelBase


class TblDiscuss(ModelBase, table_base.TableBase):
    __tablename__ = 'tbl_discuss'

    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    topic_id = Column(Integer, comment=u"话题")
    discuss = Column(Text, comment=u"评论")
    create = Column(DateTime, default=datetime.now())
    original = Column(Integer, nullable=False, default=0, comment=u"来源discuss")
    author = Column(Integer, comment=u"作者")
    status = Column(Integer, comment=u"0=正常")