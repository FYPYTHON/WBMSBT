#coding=utf-8

# 由于SQLAlchemy的对象，在数据库的session提交或关闭后，就无法使用了
# 所以这里定义一个非SQLAlchemy的对象，数据自动从SQLAlchemy对象生成

class NonDBObject:
    def __init__(self, db_obj):
        attrs = db_obj.__class__.__dict__

        for attr_name, attr in attrs.iteritems():
            if "InstrumentedAttribute" in str(type(attr)):
                setattr(self, attr_name, getattr(db_obj, attr_name))
