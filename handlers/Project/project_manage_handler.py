# coding=utf-8
from database.tbl_project import TblProject
from database.tbl_account import TblAccount
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
import weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord


def get_project_list(self):
    projects = self.mysqldb().query(TblProject).filter_by(status=0).order_by(TblProject.created_time).all()
    return projects


def get_project_by_id(self, uid):
    project = self.mysqldb().query(TblProject).filter_by(id=uid).first()
    return project

class ProjectListHandler(BaseHandler):
    # @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        projects = get_project_list(self)
        return self.render('project/projectlist.html', projects=projects)
    # @authenticated
    def post(self):
        pass


class ProjectAddHandler(BaseHandler):
    # @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        return self.render('project/projectadd.html',message="")

    # @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        cur_login_name = self.get_secure_cookie('user_account')
        cur_user_id = self.mysqldb().query(TblAccount.id,TblAccount.userstate).filter(TblAccount.username == cur_login_name).first()

        project_name = self.get_argument("project_name",None)
        top_project_id = self.get_argument("top_project_id",0)
        project_describe = self.get_argument("project_describe",None)
        msg = ''
        try:
            new_project = TblProject()
            new_project.project_name = project_name
            new_project.progress= 0
            new_project.describe = project_describe
            new_project.status = msg_define.USER_NORMAL
            new_project.top_project_id = top_project_id
            new_project.created_by = cur_user_id
            self.mysqldb().add(new_project)
            self.mysqldb().commit()
            return self.render('project/projectlist.html', projects=get_project_list(self))
        except:
            weblog.exception("Add new Project error!")
            self.mysqldb().rollback()
            return self.render('project/projectlist.html', message=msg, projects=get_project_list(self))


class ProjectEditHandler(BaseHandler):
    # @authenticated
    def get(self,id):
        weblog.info("%s.", self._request_summary())
        return self.render('admin/Projectedit.html',message="" ,project = get_project_by_id(self,id))

    # @authenticated
    def post(self,id):
        weblog.info("%s.", self._request_summary())
        Projectname = self.get_argument("Projectname", None)
        passowrd = self.get_argument("passowrd", None)
        Projectemail = self.get_argument("Projectemail", None)
        Projectrole = self.get_argument("Projectrole")
        msg = []
        if Projectname is None or Projectname == "":
            msg.append(msg_define.ProjectNAME_IS_EMPTY)
        if passowrd is None or check_passord(passowrd) is None:
            msg.append(msg_define.ProjectPASSWORD_INVALID)
        if Projectemail is None or Projectemail == "":
            msg.append(msg_define.ProjectEMAIL_IS_EMPTY)
        elif check_email(Projectemail) is None:
            msg.append(msg_define.ProjectEMAIL_INVALID)
        if msg:
            return self.render('admin/Projectedit.html', message=msg)
        else:
            try:
                old_Project = get_project_by_id(self,id)
                old_Project.Projectname = Projectname
                old_Project.password = passowrd
                old_Project.email = Projectemail
                old_Project.Projectrole = Projectrole
                self.mysqldb().commit()
                return self.redirect('/Project/list')
            except:
                weblog.exception("Edit Project error!")
                self.mysqldb().rollback()
                return self.render('admin/Projectedit.html', message=msg)


class ProjectDeleteHandler(BaseHandler):

    # @authenticated
    def get(self,id):
        weblog.info("%s.", self._request_summary())
        project = self.mysqldb().query(TblProject).filter_by(id=id).first()
        project.Projectstate = 1
        self.mysqldb().commit()
        return self.redirect('/Project/list')
