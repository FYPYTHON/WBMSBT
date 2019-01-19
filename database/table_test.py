from database.db_config import db_session
from database.tbl_account import TblAccount
from handlers.common_handler import PAGESIZE,FIRST_PAGE
if __name__ == "__main__":
    a = db_session.query(TblAccount).filter(TblAccount.id ==10)
    print(len(a.all()))
    a = a.all()


    users = db_session.query(TblAccount).filter_by(userstate=0).order_by(TblAccount.register_time.desc())
    total_page = len(users.all())//PAGESIZE + 1
    current_page = 1
    users = users.limit(PAGESIZE).offset((current_page - 1) * PAGESIZE)
    print(users, total_page)
    for us in users:
        print(us)
