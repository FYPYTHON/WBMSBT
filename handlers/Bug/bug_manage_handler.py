# coding=utf-8
from database.tbl_project import TblProject
from database.tbl_bug_list import TblBugList
from database.tbl_account import TblAccount
from database.tbl_project_user import TblPorjectUser
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
from tornado.log import access_log as weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord
from handlers.user_manage_handler import get_user_list, get_user_by_id
from handlers.Project.project_manage_handler import get_project_list

def get_bug_list(self):
    bugs = self.mysqldb().query(TblBugList.bug_name
                                , TblBugList.bug_describe
                                , TblBugList.bug_solution
                                , TblBugList.bug_id
                                , TblBugList.bug_date_plan
                                , TblBugList.bug_date_done
                                , TblBugList.bug_status
                                , TblBugList.bug_user_done
                                , TblProject.project_name.label('bug_project_id')
                                , TblAccount.username.label('bug_find_by')
                                )
    bugs = bugs.filter(TblBugList.bug_find_by == TblAccount.id
                       , TblBugList.bug_project_id == TblProject.project_id)
    bugs = bugs.order_by(TblBugList.bug_date_plan).all()
    # for project in projects:
    #     print(project.describe,type(project.describe))
    result = gene_bugs_result(self, bugs)
    return result

def gene_bugs_result(self, bugs):
    result = []
    for bug in bugs:
        bug_dict = dict()
        bug_dict['bug_id'] = bug.bug_id
        bug_dict['bug_name'] = bug.bug_name
        bug_dict['bug_describe'] = bug.bug_describe
        bug_dict['bug_solution'] = bug.bug_solution
        bug_dict['bug_solution'] = bug.bug_solution
        bug_dict['bug_date_plan'] = str(bug.bug_date_plan)
        bug_dict['bug_date_done'] = str(bug.bug_date_done)
        bug_dict['bug_status'] = bug.bug_status
        bug_dict['bug_user_done'] = bug.bug_user_done
        user = get_user_by_id(self, bug.bug_user_done)
        if user is not None:
            bug_dict['bug_user_done'] = user.username
        bug_dict['bug_project_id'] = bug.bug_project_id
        bug_dict['bug_find_by'] = bug.bug_find_by
        result.append(bug_dict)
    return result


def get_bug_by_id(self, uid):
    bug = self.mysqldb().query(TblBugList.bug_name
                                , TblBugList.bug_describe
                                , TblBugList.bug_solution
                                , TblBugList.bug_id
                                , TblBugList.bug_date_plan
                                , TblBugList.bug_date_done
                                , TblBugList.bug_status
                                , TblBugList.bug_user_done
                                , TblProject.project_name.label('bug_project_id')
                                , TblAccount.username.label('bug_find_by')
                               ).filter(TblBugList.bug_id == uid,
                                        TblBugList.bug_find_by == TblAccount.id).first()

    result = gene_bug_result(self, bug)
    return result


def gene_bug_result(self, bug):
    bug_dict = dict()
    bug_dict['bug_id'] = bug.bug_id
    bug_dict['bug_name'] = bug.bug_name
    bug_dict['bug_describe'] = bug.bug_describe
    bug_dict['bug_solution'] = bug.bug_solution
    bug_dict['bug_solution'] = bug.bug_solution
    bug_dict['bug_date_plan'] = str(bug.bug_date_plan)
    bug_dict['bug_date_done'] = str(bug.bug_date_done)
    bug_dict['bug_status'] = bug.bug_status
    bug_dict['bug_user_done'] = bug.bug_user_done
    user = get_user_by_id(self, bug.bug_user_done)
    if user is not None:
        bug_dict['bug_user_done'] = user.username
    bug_dict['bug_project_id'] = bug.bug_project_id
    bug_dict['bug_find_by'] = bug.bug_find_by
    return bug_dict


class BugListHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        bugs = get_bug_list(self)
        return self.render('bug/buglist.html', bugs=bugs)

    @authenticated
    def post(self):
        pass


class BugAddHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        return self.render('bug/bugadd.html',message="", users=get_user_list(self)
                           ,projects=get_project_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        cur_login_name = self.get_secure_cookie('user_account')
        # 用户是否存在
        bug_name = self.get_argument("bug_name",None)
        project_id = self.get_argument("project_name", None)
        bug_find_by = self.get_argument("bug_find_by", None)
        bug_user_done = self.get_argument("bug_user_done", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        msg = []
        if bug_name is None:
            msg.append(u"bug名称不能为空")
        if bug_solution is None or bug_describe is None:
            msg.append(u"bug描述或解决方案为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"bug计划日期或解决日期为空")
        if msg:
            return self.render('bug/bugadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        try:
            new_bug = TblBugList()
            new_bug.bug_name = bug_name
            new_bug.bug_find_by = bug_find_by
            new_bug.bug_user_done = bug_user_done
            new_bug.bug_describe = bug_describe
            new_bug.bug_solution = bug_solution
            new_bug.bug_date_plan = bug_date_plan
            new_bug.bug_date_done = bug_date_done
            new_bug.bug_project_id = project_id
            self.mysqldb().add(new_bug)
            self.mysqldb().commit()
            return self.render('bug/buglist.html', bugs=get_bug_list(self))
        except:
            weblog.exception("Add new bug error!")
            self.mysqldb().rollback()
            return self.render('bug/bugadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))

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


class BugEditHandler(BaseHandler):
    @authenticated
    def get(self, id):
        weblog.info("%s.", self._request_summary())
        return self.render('bug/bugedit.html', message="", bug=get_bug_by_id(self, id))

    @authenticated
    def post(self, id):
        weblog.info("%s.", self._request_summary())
        bug_name = self.get_argument("bug_name", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_date_plan = self.get_argument("bug_date_plan",None)
        bug_date_done = self.get_argument("bug_date_done",None)
        bug_status = self.get_argument("bug_status", None)
        # print(bug_name, bug_describe, bug_status)
        msg = []
        if bug_name is None:
            msg.append(u"bug名称不能为空")
        if bug_describe is None or bug_solution is None:
            msg.append(u"bug描述或解决方案不能空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"bug计划解决日期或解决日期不能为空")
        if bug_status is None:
            msg.append(u"bug状态不能为空")
        else:
            bug_status = int(bug_status)
        old_bug = self.mysqldb().query(TblBugList).filter_by(bug_id=id).first()
        if old_bug is None:
            msg.append(u"根据bug id获取bug信息失败")
        if msg:
            return self.render('bug/bugedit.html', message=msg, bug=get_bug_by_id(self, id))
        else:
            try:
                # edit_bug = get_bug_by_id(self,id)
                old_bug.bug_name = bug_name
                old_bug.bug_describe = bug_describe
                old_bug.bug_solution = bug_solution
                old_bug.bug_date_plan = bug_date_plan
                old_bug.bug_date_done = bug_date_done
                old_bug.bug_status = bug_status
                # print(bug_status, bug_describe)
                self.mysqldb().commit()
                return self.redirect('/bug/list')
            except Exception as e:
                weblog.exception("Edit Bug error!", e)
                self.mysqldb().rollback()
                msg.append(e)
                return self.render('bug/bugedit.html', message=msg)


class BugDeleteHandler(BaseHandler):
    @authenticated
    def get(self,id):
        weblog.info("%s.", self._request_summary())
        project = self.mysqldb().query(TblProject).filter_by(id=id).first()
        project.Projectstate = 1
        self.mysqldb().commit()
        return self.redirect('/Project/list')
