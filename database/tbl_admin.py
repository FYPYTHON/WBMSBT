# coding=utf-8

from sqlalchemy import Column, String, Integer, DateTime, BLOB
from database import table_base
from database.db_config import ModelBase


class TblAdmin(ModelBase, table_base.TableBase):
    __tablename__ = 'tbl_admin'
    
    id = Column(Integer, unique=True, primary_key=True)
    name = Column(String(60), unique=True, comment=u"变量名")
    value = Column(String(60))
    type = Column(Integer)

    def __repr__(self):
        return "%s<id=%s, name=%s,value=%s>" % (self.__class__.__name__, self.id, self.name,self.value)

