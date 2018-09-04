# coding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

ModelBase = declarative_base()
engine = create_engine('mysql+pymysql://root:Faye0808@localhost:3306/faye_dream?charset=utf8',pool_size=100,echo=False)

session_factory = sessionmaker(bind = engine)
db_session = scoped_session(session_factory)

# test code
if __name__ == "__main__":

    from database.tbl_admin import TAdmin
    result = db_session.query(TAdmin).all()
    passsword = TAdmin()
    passsword.name = "__TEXT__"
    passsword.value = "text"
    passsword.type = 1
    db_session.add(passsword)
    # db_session.commit()
    for res in result:
        print(res)



