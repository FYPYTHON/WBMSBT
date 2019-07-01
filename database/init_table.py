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

def init_setting():
    from database.tbl_admin import TblAdmin
    db_session.add_all([
    TblAdmin(name="currentname",value="feiying",type=0),
    TblAdmin(name="description",value="test only",type=0),
    TblAdmin(name="admin_email", value="1490726887@qq.com", type=0),
    TblAdmin(name="can_register", value="1", type=1),
    TblAdmin(name="can_comment", value="1", type=1),
    TblAdmin(name="comments_notify", value="1", type=1),
    TblAdmin(name="default_category", value="default_category", type=0),
    TblAdmin(name="page_size", value="10", type=1),
    TblAdmin(name="rss_size", value="10", type=1),
    TblAdmin(name="rss_excerpt", value="1", type=1),
    TblAdmin(name="new_rss_size", value="5", type=1),
    TblAdmin(name="new_page_size", value="5", type=1),
    ])

    db_session.commit()



if __name__ == "__main__":
    # init_admin()
    # init_user()
    # init_setting()
    from database.tbl_bug_list import TblBugList
    from database.tbl_project import TblProject
    from database.tbl_account import TblAccount
    # done_user = db_session.query(TblAccount).subquery()
    bugs = db_session.query(TblBugList.bug_name
                                , TblBugList.bug_describe
                                , TblBugList.bug_solution
                                , TblBugList.bug_id
                                , TblBugList.bug_date_plan
                                , TblBugList.bug_date_done
                                , TblBugList.bug_status
                                , TblProject.project_name.label('bug_project_id')
                                , TblAccount.username.label('bug_find_by')
                                )
    bugs = bugs.filter(TblBugList.bug_find_by == TblAccount.id
                       , TblBugList.bug_project_id == TblProject.project_id)
    bugs = bugs.order_by(TblBugList.bug_date_plan).all()

    for bug in bugs:
        print(bug)