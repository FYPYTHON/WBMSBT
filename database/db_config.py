# coding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
# import pymysql
# pymysql.install_as_MySQLdb()

ModelBase = declarative_base()
engine = create_engine('mysql+pymysql://root:Faye0808@localhost:3306/faye_dream?charset=utf8',pool_size=100,echo=False)
# Session = sessionmaker(bind=engine)
# db_session = Session()


session_factory = sessionmaker(bind = engine)
db_session = scoped_session(session_factory)

if __name__ == "__main__":
    print("ok")
    from database.t_admin import TAdmin
    result = db_session.query(TAdmin).all()
    passsword = TAdmin()
    passsword.name = "__TEXT__"
    passsword.value = "text"
    passsword.type = 1
    db_session.add(passsword)
    # db_session.commit()
    for res in result:
        print(res)



