# coding=utf-8
from json import dumps
from database.tbl_account import TblAccount
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
import weblog
from message import msg_define
from method.data_encode import MD5
from handlers.Email.email_smtp_handler import check_email, check_passord
from handlers.common_handler import get_pages, PAGESIZE, FIRST_PAGE
from message.msg_serialize import PageInfoList, UserInfo


def get_user_list(self):
    users = self.mysqldb().query(TblAccount).filter_by(userstate=0, userrole=0).order_by(TblAccount.register_time.desc()).all()
    return users


def get_user_pagination(self,current_page):
    users = self.mysqldb().query(TblAccount).filter_by(userstate=0).order_by(TblAccount.register_time.desc())
    total_count = len(users.all())
    total_page = get_pages(total_count)
    users = users.limit(PAGESIZE).offset((current_page-1)*PAGESIZE)
    return users, total_page


def get_user_by_id(self, uid):
    user = self.mysqldb().query(TblAccount).filter_by(id=uid).first()
    return user


def get_user_by_name(self, name):
    user = self.mysqldb().query(TblAccount).filter_by(username=name).first()
    return user


class UserListHandler(BaseHandler):
    @authenticated
    def get(self):
        current_page = int(self.get_argument("current_page", FIRST_PAGE))
        # users = get_user_list(self)
        users, total_page = get_user_pagination(self, current_page)
        weblog.info("{2}. user list total page:{0},current page:{1}".format(
            total_page, current_page, self._request_summary()))
        return self.render('admin/usermanage.html', users=users,
                           current_page=current_page, total_page=total_page)

    @authenticated
    def post(self):
        current_page = int(self.get_argument("current_page", FIRST_PAGE))
        # users = get_user_list(self)
        users, total_page = get_user_pagination(self, current_page)

        weblog.info("{2}. user list total page:{0},current page:{1}".format(
                        total_page, current_page, self._request_summary()))
        data = PageInfoList()
        for user in users:
            userinfo = UserInfo()
            userinfo.username = user.username
            userinfo.id = user.id
            userinfo.password = user.password
            userinfo.email = user.email
            userinfo.userstate = user.userstate
            userinfo.userrole = user.userrole
            userinfo.register_time = str(user.register_time)
            userinfo.avatar_path = user.avatar_path
            data.datalist.append(userinfo)
        data.current_page = current_page
        data.total_page = total_page
        data.page_size = PAGESIZE

        return self.write(data.serialize())


class UserAddHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        return self.render('admin/useradd.html',message="")

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        username = self.get_argument("username",None)
        passowrd = self.get_argument("passowrd",None)
        useremail = self.get_argument("useremail",None)
        userrole = self.get_argument("userrole")
        msg = []
        if get_user_by_name(self,username) is not None:
            msg.append(msg_define.USER_IS_EXIST)
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
                new_user.password = MD5(passowrd)
                new_user.email = useremail
                new_user.userrole = userrole
                new_user.userstate = msg_define.USER_NORMAL
                self.mysqldb().add(new_user)
                self.mysqldb().commit()
                users, total_page = get_user_pagination(self, FIRST_PAGE)
                return self.render('admin/usermanage.html', users=users,
                                   total_page=total_page, current_page=FIRST_PAGE)
            except:
                weblog.exception("Add new user error!")
                self.mysqldb().rollback()
                return self.render('admin/useradd.html', message=msg)


class UserEditHandler(BaseHandler):
    @authenticated
    def get(self,id):
        weblog.info("%s.", self._request_summary())
        return self.render('admin/useredit.html',message="" ,user = get_user_by_id(self,id))

    @authenticated
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
    @authenticated
    def get(self,id):
        weblog.info("%s.", self._request_summary())
        user = self.mysqldb().query(TblAccount).filter_by(id=id).first()
        user.userstate = 1
        self.mysqldb().commit()
        return self.redirect('/user/list')
