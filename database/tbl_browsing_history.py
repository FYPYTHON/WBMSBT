# coding=utf-8

from sqlalchemy import Column, String, Integer , DateTime

from database import table_base
from database.db_config import ModelBase


# web访问历史记录
class TblBrowsingHistory(ModelBase, table_base.TableBase):
    __tablename__ = 'tbl_browsing_history'

    id = Column(Integer, unique=True, primary_key=True)
    user_ip = Column(String(100))         # 访问ip
    user_account = Column(String(100))    # 登录用户
    uri = Column(String(255))             # 访问地址

    request_method = Column(String(100))  # post/get
    status = Column(String(100))          # 访问状态码
    browsing_date = Column(String(20))   # 访问日期
    browsing_time = Column(String(20))    # 访问时间
    user_agent = Column(String(200))        # 用户代理

    def __repr__(self):
        return "%s<id=%s, ip=%s>" % (self.__class__.__name__, self.id, self.ip)

