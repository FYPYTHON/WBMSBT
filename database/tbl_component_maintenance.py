# coding=utf-8
from database.table_base import TableBase
from database.db_config import ModelBase
from datetime import datetime
from sqlalchemy import Column, Integer, String, TEXT, DATETIME


# 模块名称	维护人姓名	模块维护方式（增加新功能/问题排查）	新功能内容	问题是否解决	问题描述	问题原因	解决方式	备注
class TblComponentMaintenance(ModelBase, TableBase):
    __tablename__ = "tbl_component_maintenance"
    comp_id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    comp_belong_to = Column(Integer, default=0, comment="user belong to this component")  # 任务
    comp_type = Column(Integer, nullable=False, comment=u"0=增加新功能,1=问题排查,2=优化调整,3=其他")  # 用户
    comp_new = Column(TEXT, comment=u"新功能内容")        # 计划安排描述
    comp_status = Column(Integer, nullable=False, default=0, comment=u"0=未解决,1=已解决")
    comp_describe = Column(TEXT, comment=u"问题描述")
    comp_reason = Column(TEXT, comment=u"问题原因")
    comp_solution = Column(TEXT, comment=u"解决方式")
    create_time = Column(DATETIME, default=datetime.now())
    modify_time = Column(DATETIME, default=datetime.now())
    comment = Column(String(256), comment=u"备注,不超过200字") #完成情况说明

