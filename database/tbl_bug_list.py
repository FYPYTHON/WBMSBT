# coding=utf-8
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, func, Text, Date
from database import table_base
from database.db_config import ModelBase
# created_time project_name project_id describe sub_project_id created_by(id)  progress(int) status peer


class TblBugList(ModelBase, table_base.TableBase):
    __tablename__ = 'tbl_bug_list'
    bug_id = Column(Integer, primary_key=True, autoincrement=True,unique=True)
    bug_find_by = Column(Integer, nullable=False)
    bug_name = Column(String(1024), nullable=False)
    bug_describe = Column(Text, default='')
    bug_solution = Column(Text, default='')
    bug_date_plan = Column(Date)
    bug_date_done = Column(Date)
    bug_user_done = Column(Integer, nullable=False)
    bug_project_id = Column(Integer, nullable=False)
    bug_status = Column(Integer,comment='0=on,1=off')

