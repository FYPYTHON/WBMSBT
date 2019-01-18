from database.db_config import db_session
from database.tbl_account import TblAccount

if __name__ == "__main__":
    a = db_session.query(TblAccount).all()
    for i in a:
        print(i)