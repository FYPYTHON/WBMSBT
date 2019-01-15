#!/usr/bin/env python
# coding=utf-8

import hashlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def clear_db():

    engine = create_engine('mysql+pymysql://root:Faye0808@localhost:3306/?charset=utf8')
    Session = sessionmaker(bind=engine)
    db_session = Session()

    print( "drop database....")
    db_session.execute('drop database if EXISTS faye_dream;')
    db_session.execute('create database faye_dream default charset utf8 collate utf8_general_ci;')


def create_table():

    import os.path
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    for root, dirs, files in os.walk("."):
        root = root.strip(".%s" % os.path.sep)
        for f in files:
            if f.startswith("tbl_") and f.endswith(".py"):
                py_module = os.path.join(root, f[:-3]).replace(os.path.sep, ".")
                cmd =  "import %s" % py_module
                print (cmd,py_module,f[:-3])
                exec(cmd)

    from database import db_config

    print ("drop table....")
    db_config.ModelBase.metadata.drop_all(db_config.engine)

    print ("create table....")
    db_config.ModelBase.metadata.create_all(db_config.engine)

    print ("done!")


def create_single_table():
    # from database import tbl_project
    # from database import tbl_project_progress
    from database import tbl_project_user
    from database import db_config
    print("create table....")
    db_config.ModelBase.metadata.create_all(db_config.engine)

def init_data():
    print ('init_data...')
    from database.db_config import db_session
    from database.tbl_admin import TblAdmin
    user = TblAdmin()
    user.name = "__MAIL__"
    user.value = "1823218990@qq.com"
    user.type = 1
    email = TblAdmin()
    email.name = "__MAILPASSWORD__"
    email.value = "xxxxxxxxxx"
    email.type = 1
    user_exist = db_session.query(TblAdmin.name).filter(TblAdmin.name == user.name).first()
    if user_exist is None:
        db_session.add(user)

    mail_exist = db_session.query(TblAdmin.name).filter(TblAdmin.name == email.name).first()
    if mail_exist is None:
        db_session.add(email)
    db_session.commit()
    db_session.close()


    print ("done!")

def init_account():
    print ('init one account...')
    from database.db_config import db_session
    from database.tbl_account import TblAccount
    from method.data_encode import MD5
    account = TblAccount()
    account.username = "a123456"
    account.password = MD5("123456")
    account.userrole = 0
    account.email = "1823218990@qq.com"
    db_session.add(account)
    db_session.commit()
    db_session.close()
    print("add ok")

if __name__ == '__main__':
    # clear_db()
    # create_table()
    # init_account()
    # init_data()
    create_single_table()



