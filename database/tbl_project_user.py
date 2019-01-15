# coding=utf-8
from database.table_base import TableBase
from database.db_config import ModelBase
from sqlalchemy import Column,Integer,ForeignKey
from database.tbl_project import TblProject
from database.tbl_account import TblAccount


class TblPorjectUser(ModelBase, TableBase):
    __tablename__ = "tbl_project_user"
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    # company = relationship("Company", backref="phone_of_company")
    project_id = Column(Integer, ForeignKey("tbl_project.project_id"), nullable=False)
    account_id = Column(Integer, ForeignKey("tbl_account.id"), nullable=False)
    # account_id = Column(Integer, nullable=False, comment="user id")
