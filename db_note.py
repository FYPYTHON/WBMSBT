# coding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import pymysql
import redis
redis_session = redis.StrictRedis(host='localhost', port=6379, password='feiying')
pymysql.install_as_MySQLdb()
ModelBase = declarative_base()
engine = create_engine('mysql+pymysql://root:Faye0808@localhost:3306/faye_dream?charset=utf8',pool_size=100,echo=False)

session_factory = sessionmaker(bind=engine)
db_session = scoped_session(session_factory)

def init_comp_mt():
    from database.tbl_component_maintenance import TblComponentMaintenance
    from datetime import datetime
    tcm = TblComponentMaintenance()
    tcm.comment = ""
    tcm.user_belong_to = 5
    tcm.comp_belong_to = 4
    tcm.comp_describe = ""
    tcm.comp_new = "add new content cc"
    tcm.comp_reason = ""
    tcm.comp_solution = ""
    tcm.comp_status = 0
    tcm.comp_type = 0
    tcm.create_time = datetime.now()
    tcm.modify_time = datetime.now()
    db_session.add(tcm)
    db_session.commit()

# test code
if __name__ == "__main__":
    # from database.tbl_bug_list import TblBugList
    # result = db_session.query(TblBugList).all()
    # print(len(result))
    # for res in result:
    #     print(res)
    # a = redis_session.keys()
    # print(a)
    import time
    t1 = time.time()
    redis_session.set("test", "123", 6)
    # print(redis_session.get("test"))
    name = redis_session.keys('*')
    # print(redis_session.keys('*'))
    redis_session.delete('test')

    for na in name:

        print(na, redis_session.get(na))

    user = True
    if not user:
        print("ok?")
    else:
        print("not ok?")

    print(time.time() - t1)









