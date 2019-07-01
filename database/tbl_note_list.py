# coding=utf-8
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, func, Text
from database import table_base
from database.db_config import ModelBase


class TblPostList(ModelBase, table_base.TableBase):
    __tablename__ = 'tbl_post_list'

    id = Column(Integer, primary_key=True, autoincrement=True)
    # this post will be published in this 'parent' page
    parent = Column(Integer, default=0, nullable=False)
    author = Column(Integer, default=0)
    date = Column(DateTime, default=func.now())
    modified = Column(DateTime, default=func.now(), onupdate=datetime.now)
    title = Column(Text, default='', nullable=False)
    content = Column(Text, default='')
    excerpt = Column(Text, default='')
    status = Column(String(20), default='enabled')
    comment_status = Column(String(20), default='enabled')
    authorname = Column(String(32), default='')
    # password = Column(String(32), default='')
    guid = Column(String(255), default='')
    # type: page, post
    type = Column(String(20), default='post')
    # when it's a page, it will be ordered by 'order'
    order = Column(Integer, default=0)
    # mime_type:
    mime_type = Column(String(20), default='')
    comment_count = Column(Integer, default=0)

    def __repr__(self):
        return "%s<id=%s, title=%s>" % (self.__class__.__name__, self.id, self.title)
