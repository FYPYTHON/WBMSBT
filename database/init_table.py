# coding=utf-8
import hashlib

from database.db_config import db_session
from method.data_encode import MD5
def init_admin():
    from database.tbl_admin import TblAdmin
    user = TblAdmin()
    user.name = "__MAIL__"
    user.value = "1490726887@qq.com"
    user.type = 1
    db_session.add(user)
    db_session.commit()
    db_session.close()

def init_user():
    from database.tbl_account import TblAccount
    account = TblAccount()
    account.username = "TestAccount"
    account.password = MD5("111111")
    account.email = "1490726887@qq.com"
    account.userstate = 0
    account.userrole = 0
    db_session.add(account)
    db_session.commit()
    db_session.close()

if __name__ == "__main__":
    init_admin()
    init_user()