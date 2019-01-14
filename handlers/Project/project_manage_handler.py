# coding=utf-8
from database.tbl_project import TblProject
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
import weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord

def get_project_list(self):
    projects = self.mysqldb().query(TblProject).filter_by(userstate=0).order_by(TblProject.id).all()
    return projects


def get_project_by_id(self, uid):
    project = self.mysqldb().query(TblProject).filter_by(id=uid).first()
    return project


class ProjectListHandler(BaseHandler):
    # @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        projects = get_project_list()
        return self.render('project/projectlist.html', Projects=projects)
    # @authenticated
    def post(self):
        pass


class ProjectAddHandler(BaseHandler):
    # @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        return self.render('admin/Projectadd.html',message="")

    # @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        Projectname = self.get_argument("Projectname",None)
        passowrd = self.get_argument("passowrd",None)
        Projectemail = self.get_argument("Projectemail",None)
        msg = []
        if Projectname is None or Projectname=="":
            msg.append(msg_define.ProjectNAME_IS_EMPTY)
        if passowrd is None or check_passord(passowrd) is None:
            msg.append(msg_define.ProjectPASSWORD_INVALID)
        if Projectemail is None or Projectemail == "":
            msg.append(msg_define.ProjectEMAIL_IS_EMPTY)
        elif check_email(Projectemail) is None:
            msg.append(msg_define.ProjectEMAIL_INVALID)
        if msg:
            return self.render('admin/Projectadd.html',message=msg)
        else:
            try:
                new_Project = TblProject()
                new_Project.project_name = Projectname
                new_Project.progress= msg_define.Project_NORMAL
                self.mysqldb().add(new_Project)
                self.mysqldb().commit()
                return self.render('admin/Projectmanage.html', Projects=get_project_list(self))
            except:
                weblog.exception("Add new Project error!")
                self.mysqldb().rollback()
                return self.render('admin/Projectadd.html', message=msg)


class ProjectEditHandler(BaseHandler):
    # @authenticated
    def get(self,id):
        weblog.info("%s.", self._request_summary())
        return self.render('admin/Projectedit.html',message="" ,Project = get_project_by_id(self,id))

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
