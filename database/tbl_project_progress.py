# coding=utf-8
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, func, Text
from database import table_base
from database.db_config import ModelBase
# project_id user_id comment datetime progress


class TblProjectProgress(ModelBase, table_base.TableBase):
    __tablename__ = 'tbl_project_progress'
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer)
    user_id = Column(Integer)
    modify_time = Column(DateTime, default=datetime.now())
    cur_progress = Column(Integer)       # modify current progress

    def __repr__(self):
        return "%s<id=%s, value=%s>" % (self.__class__.__name__, self.id, self.cur_progress,)
