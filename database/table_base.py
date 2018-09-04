# coding=utf-8

from sqlalchemy import and_

from database import non_db_object
from database.db_config import db_session

class TableBase:

    def save(self):
        db_session.add(self)
        db_session.commit()
        db_session.close()

    def to_non_db_obj(self):
        return non_db_object.NonDBObject(self)

    def from_non_db_obj(self, non_db_obj):

        for attr_name, attr in non_db_obj.__dict__.iteritems():
            if attr_name != "id":
                setattr(self, attr_name, attr)