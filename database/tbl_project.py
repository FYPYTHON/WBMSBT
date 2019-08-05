# coding=utf-8
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, func, Text
from database import table_base
from database.db_config import ModelBase
# created_time project_name project_id describe sub_project_id created_by(id)  progress(int) status peer


class TblProject(ModelBase, table_base.TableBase):
    __tablename__ = 'tbl_project'
    project_id = Column(Integer, primary_key=True, autoincrement=True,unique=True)
    project_name = Column(String(256), nullable=False, unique=True)
    describe = Column(Text, default='')
    top_project_id = Column(Integer)   # belong to other project
    created_by = Column(Integer)      # use id
    created_time = Column(DateTime, default=datetime.now(),onupdate=datetime.now())
    progress = Column(Integer, )        # progress of the project
    status = Column(Integer,comment='0=enable,1=disable')          # 0=enable,1=disable

    def __repr__(self):
        return "%s<id=%s, name=%s,value=%s>" % (self.__class__.__name__, self.project_id, self.project_name, self.status)

