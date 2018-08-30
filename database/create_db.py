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
    db_session.execute('create database fate_dream default charset utf8 collate utf8_general_ci;')


def create_table():

    import os.path
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    for root, dirs, files in os.walk("."):
        root = root.strip(".%s" % os.path.sep)
        for f in files:
            if f.startswith("t_") and f.endswith(".py"):
                py_module = os.path.join(root, f[:-3]).replace(os.path.sep, ".")
                cmd =  "import %s" % py_module
                print (cmd)
                exec(cmd)

    from database import db_config
    print ("drop table....")
    db_config.ModelBase.metadata.drop_all(db_config.engine)

    print ("create table....")
    db_config.ModelBase.metadata.create_all(db_config.engine)

    print ("done!")



def init_data():
    print ('init_data...')
    from database.db_config import db_session
    from database.t_admin import TAdmin
    user = TAdmin()
    user.name = "__MAIL__"
    user.value = "xxxx@qq.com"
    user.type = 1
    db_session.add(user)
    db_session.commit()


    print ("done!")


if __name__ == '__main__':
    # clear_db()
    # create_table()
    init_data()

