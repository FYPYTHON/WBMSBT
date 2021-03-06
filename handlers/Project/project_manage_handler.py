# coding=utf-8
from database.tbl_project import TblProject
from database.tbl_account import TblAccount
from database.tbl_project_user import TblPorjectUser
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
from tornado.log import access_log as weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord
from handlers.user_manage_handler import get_user_list


def get_project_list(self):
    projects = self.mysqldb().query(TblProject).filter_by(status=0).order_by(TblProject.created_time.desc()).all()
    # for project in projects:
    #     print(project.describe,type(project.describe))
    return projects


def get_project_map(self):
    projects = self.mysqldb().query(TblProject.project_id, TblProject.project_name).filter_by(status=0).all()
    project_map = dict()
    project_map[0] = None
    for project in projects:
        project_map[project.project_id] = project.project_name
    return project_map


def get_project_by_id(self, uid):
    project = self.mysqldb().query(TblProject).filter_by(project_id=uid).first()
    return project


class ProjectListHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        projects = get_project_list(self)
        project_map = get_project_map(self)
        return self.render('project/projectlist.html', projects=projects, project_map=project_map)

    @authenticated
    def post(self):
        pass


class ProjectAddHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        return self.render('project/projectadd.html',message="", users=get_user_list(self)
                           , projects=get_project_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        cur_login_name = self.get_secure_cookie('user_account')
        # 用户是否存在
        cur_user_id = self.mysqldb().query(TblAccount.id, TblAccount.userstate).filter(
                                            TblAccount.username == cur_login_name).first()
        project_name = self.get_argument("project_name", None)
        top_project_id = self.get_argument("top_project_id", 0)
        project_describe = self.get_argument("project_describe", None)
        peers = self.get_arguments("peer")
        msg = ''
        try:
            new_project = TblProject()
            new_project.project_name = project_name
            new_project.progress = 0
            new_project.describe = project_describe
            new_project.status = msg_define.USER_NORMAL
            new_project.top_project_id = top_project_id
            new_project.created_by = cur_user_id.id
            self.mysqldb().add(new_project)
            self.mysqldb().commit()
            # 添加项目关联人员
            self.relation_project_user(project_name, peers)
            # return self.render('project/projectlist.html', projects=get_project_list(self),
            #                    project_map=get_project_map(self))
            return self.redirect('/project/list')
        except:
            weblog.exception("Add new Project error!")
            self.mysqldb().rollback()
            return self.render('project/projectadd.html', message="", users=get_user_list(self)
                               , projects=get_project_list(self))

    def relation_project_user(self, project_name, peers):
        project_id = self.mysqldb().query(TblProject.project_id,TblProject.top_project_id).filter(
                                            TblProject.project_name==project_name).first()
        if project_id is None:
            return msg_define.FAIL
        for peer in peers:
            # print("peer:",peer)
            relation = TblPorjectUser()
            relation.project_id = project_id.project_id
            relation.account_id = int(peer)
            relation_is_exist = self.mysqldb().query(TblPorjectUser).filter(
                                            TblPorjectUser.project_id == project_id.project_id
                                            , TblPorjectUser.account_id == int(peer)).first()
            if relation_is_exist is None:
                self.mysqldb().add(relation)
        self.mysqldb().commit()
        return msg_define.SUCCESS


class ProjectEditHandler(BaseHandler):
    @authenticated
    def get(self, id):
        weblog.info("%s.", self._request_summary())
        return self.render('admin/projectedit.html', message="", project=get_project_by_id(self, id))

    @authenticated
    def post(self, id):
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
    @authenticated
    def get(self, pjid):
        weblog.info("%s. pjid=%d", self._request_summary(), pjid)
        project = self.mysqldb().query(TblProject).filter_by(project_id=pjid).first()   # u"必须查询对象"
        # print(project)
        try:
            project.status = 1
            self.mysqldb().commit()
        except Exception as e:
            weblog.error("delete project id={} fail:{}.".format(pjid, e))
            self.mysqldb().rollback()
        return self.redirect('/project/list')
        # projects = get_project_list(self)
        # project_map = get_project_map(self)
        # return self.render('project/projectlist.html', projects=projects, project_map=project_map)
