# coding=utf-8
from database.table_base import TableBase
from database.db_config import ModelBase
from sqlalchemy import Column, Integer, String, TEXT, DATETIME


class TblPorjectUser(ModelBase, TableBase):
    __tablename__ = "tbl_weekpost"
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    task = Column(Integer, default=0, comment="task to finish") # 任务
    user = Column(Integer, nullable=False, comment="poster")  # 用户
    post_content = Column(TEXT)        # 计划安排描述
    create_time = Column(DATETIME)
    modify_time = Column(DATETIME)
    do_dercribe = Column(String(256), comment="describe") #完成情况说明

