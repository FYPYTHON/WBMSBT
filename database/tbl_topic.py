# coding=utf-8

from sqlalchemy import Column, String, Integer,DateTime, Text
from datetime import datetime
from database import table_base
from database.db_config import ModelBase


class TblTopic(ModelBase, table_base.TableBase):
    __tablename__ = 'tbl_topic'

    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    author = Column(Integer, nullable=False)
    title = Column(String(128), nullable=False, comment=u"标题")
    content = Column(Text, comment=u"内容")
    discuss = Column(Integer, comment=u"回复")
    likes = Column(Integer, default=0, comment=u"点赞")
    status = Column(Integer, default=0, comment=u"0=正常，1=删除")
    category = Column(Integer, default=0, comment=u"类别")
    create = Column(DateTime, default=datetime.now())