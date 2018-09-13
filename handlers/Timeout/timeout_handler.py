from datetime import datetime
from database.db_config import db_session

class UserOnlineHandler:

    def mysqldb(self):
        return db_session

    @classmethod
    def get_online_users(self):
        print("current time",datetime.now())