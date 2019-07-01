# coding=utf-8
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, func, Text, Date
from database import table_base
from database.db_config import ModelBase
# created_time project_name project_id describe sub_project_id created_by(id)  progress(int) status peer
#										合入版本


class TblBugTrack(ModelBase, table_base.TableBase):
    __tablename__ = 'tbl_bug_track'
    bug_id = Column(Integer, primary_key=True, autoincrement=True,unique=True)
    bug_date_receive = Column(Date, comment=u"接收时间")
    bug_find_by = Column(Integer, nullable=False, comment=u"接口人")
    bug_component = Column(Integer, nullable=False, comment=u"问题所属模块")
    component_belong = Column(Integer, nullable=False, comment=u"模块维护人")
    component_community = Column(String(256), comment=u"模块社区讨论(新功能开发)")
    bug_project_id = Column(Integer, nullable=False, comment=u"项目名称")
    # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
    project_version = Column(String(16), nullable=False, comment=u"所属版本")
    bug_describe = Column(Text, default='', comment=u"问题描述")
    bug_level = Column(Integer, default=0, comment=u"优先级:0=低,1=中,2=高,3=急")
    bug_reason = Column(Text, default="", comment=u"问题原因")
    bug_solution = Column(Text, default='', comment=u"解决措施")
    bug_progress = Column(Text, default="", comment=u"进展（6/10）")
    bug_date_plan = Column(Date, comment=u"承诺解决日期")
    bug_date_done = Column(Date, comment=u"实际解决日期")
    bug_user_done = Column(Integer, nullable=False, comment=u"负责人")
    bug_version = Column(String(16), nullable=False, comment=u"所属版本")

