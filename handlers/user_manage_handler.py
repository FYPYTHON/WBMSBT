# coding=utf-8
from database.tbl_account import TblAccount
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
import weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord


def get_user_list(self):
    users = self.mysqldb().query(TblAccount).filter_by(userstate=0).order_by(TblAccount.id).all()
    return users


def get_user_by_id(self, uid):
    user = self.mysqldb().query(TblAccount).filter_by(id=uid).first()
    return user

class UserListHandler(BaseHandler):
    # @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        users = get_user_list(self)
        return self.render('admin/usermanage.html', users=users)
    # @authenticated
    def post(self):
        pass


class UserAddHandler(BaseHandler):
    # @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        return self.render('admin/useradd.html',message="")


    # @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        username = self.get_argument("username",None)
        passowrd = self.get_argument("passowrd",None)
        useremail = self.get_argument("useremail",None)
        userrole = self.get_argument("userrole")
        msg = []
        if username is None or username=="":
            msg.append(msg_define.USERNAME_IS_EMPTY)
        if passowrd is None or check_passord(passowrd) is None:
            msg.append(msg_define.USERPASSWORD_INVALID)
        if useremail is None or useremail == "":
            msg.append(msg_define.USEREMAIL_IS_EMPTY)
        elif check_email(useremail) is None:
            msg.append(msg_define.USEREMAIL_INVALID)
        if msg:
            return self.render('admin/useradd.html',message=msg)
        else:
            try:
                new_user = TblAccount()
                new_user.username = username
                new_user.password = passowrd
                new_user.email = useremail
                new_user.userrole = userrole
                new_user.userstate = msg_define.USER_NORMAL
                self.mysqldb().add(new_user)
                self.mysqldb().commit()
                return self.render('admin/usermanage.html', users=get_user_list(self))
            except:
                weblog.exception("Add new user error!")
                self.mysqldb().rollback()
                return self.render('admin/useradd.html', message=msg)


class UserEditHandler(BaseHandler):
    # @authenticated
    def get(self,id):
        weblog.info("%s.", self._request_summary())
        return self.render('admin/useredit.html',message="" ,user = get_user_by_id(self,id))

    # @authenticated
    def post(self,id):
        weblog.info("%s.", self._request_summary())
        username = self.get_argument("username", None)
        passowrd = self.get_argument("passowrd", None)
        useremail = self.get_argument("useremail", None)
        userrole = self.get_argument("userrole")
        msg = []
        if username is None or username == "":
            msg.append(msg_define.USERNAME_IS_EMPTY)
        if passowrd is None or check_passord(passowrd) is None:
            msg.append(msg_define.USERPASSWORD_INVALID)
        if useremail is None or useremail == "":
            msg.append(msg_define.USEREMAIL_IS_EMPTY)
        elif check_email(useremail) is None:
            msg.append(msg_define.USEREMAIL_INVALID)
        if msg:
            return self.render('admin/useredit.html', message=msg)
        else:
            try:
                old_user = get_user_by_id(self,id)
                old_user.username = username
                old_user.password = passowrd
                old_user.email = useremail
                old_user.userrole = userrole
                self.mysqldb().commit()
                return self.redirect('/user/list')
            except:
                weblog.exception("Edit user error!")
                self.mysqldb().rollback()
                return self.render('admin/useredit.html', message=msg)

class UserDeleteHandler(BaseHandler):


    # @authenticated
    def get(self,id):
        weblog.info("%s.", self._request_summary())
        user = self.mysqldb().query(TblAccount).filter_by(id=id).first()
        user.userstate = 1
        self.mysqldb().commit()
        return self.redirect('/user/list')
