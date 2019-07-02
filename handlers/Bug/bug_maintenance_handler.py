# coding=utf-8
import json
from datetime import datetime
from database.tbl_project import TblProject
from database.tbl_bug_list import TblBugList
from database.tbl_account import TblAccount
from database.tbl_component_maintenance import TblComponentMaintenance
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
import weblog
from message import msg_define
from handlers.user_manage_handler import get_user_list, get_user_by_id
from handlers.Project.project_manage_handler import get_project_list
from method.alchemy_encoder import new_alchemy_encoder


def get_compmt_list(self, user=None, comp=None, status=None):
    bugs = self.mysqldb().query(TblComponentMaintenance.comp_status
                                , TblComponentMaintenance.comp_solution
                                , TblComponentMaintenance.comp_reason
                                , TblComponentMaintenance.comp_new
                                , TblComponentMaintenance.create_time
                                , TblComponentMaintenance.modify_time
                                , TblComponentMaintenance.comp_type
                                , TblComponentMaintenance.comp_describe
                                , TblComponentMaintenance.comment
                                , TblAccount.username.label("user_belong_to")
                                , TblProject.project_name.label("comp_belong_to")
                                , TblComponentMaintenance.comp_id)
    bugs = bugs.filter(TblComponentMaintenance.comp_belong_to == TblProject.project_id
                       , TblComponentMaintenance.user_belong_to == TblAccount.id
                       , TblComponentMaintenance.comp_status >= 0)
    if user is not None:
        bugs = bugs.filter(TblComponentMaintenance.user_belong_to == user)
    if status is not None:
        bugs = bugs.filter(TblComponentMaintenance.comp_status == status)
    if comp is not None:
        bugs = bugs.filter(TblComponentMaintenance.comp_belong_to == comp)
    bugs = bugs.order_by(TblComponentMaintenance.create_time.desc()).all()
    return bugs


def gene_compmt_result(self, bugs):
    result = []
    for bug in bugs:
        bug_dict = dict()
        bug_dict['comp_id'] = bug.comp_id
        bug_dict['comp_type'] = bug.comp_type
        bug_dict['comp_status'] = bug.comp_status
        bug_dict['comp_solution'] = bug.comp_solution
        bug_dict['comp_reason'] = bug.comp_reason
        bug_dict['comp_new'] = bug.comp_new
        bug_dict['comp_describe'] = bug.comp_describe
        bug_dict['comment'] = bug.comment
        bug_dict['user_belong_to'] = bug.user_belong_to
        bug_dict['comp_belong_to'] = bug.comp_belong_to
        bug_dict['create_time'] = str(bug.create_time)
        bug_dict['modify_time'] = str(bug.modify_time)
        result.append(bug_dict)
    return result


def get_compmt_by_id(self, cid):
    bug = self.mysqldb().query(TblComponentMaintenance.create_time
                                , TblComponentMaintenance.modify_time
                                , TblComponentMaintenance.comp_type
                                , TblComponentMaintenance.comp_status
                                , TblComponentMaintenance.comp_solution
                                , TblComponentMaintenance.comp_reason
                                , TblComponentMaintenance.comp_new
                                , TblComponentMaintenance.comp_describe
                                , TblComponentMaintenance.comment
                                , TblAccount.username.label("user_belong_to")
                                , TblProject.project_name.label("comp_belong_to")
                                , TblComponentMaintenance.comp_id)
    bug = bug.filter(TblComponentMaintenance.comp_belong_to == TblProject.project_id
                     , TblComponentMaintenance.user_belong_to == TblAccount.id
                     , TblComponentMaintenance.comp_id == cid)
    bug = bug.first()
    return bug


class BugCompmtListHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        compmts = get_compmt_list(self)
        return self.render('bug/compmtlist.html', bugs=compmts,
                           users=get_user_list(self), projects=get_project_list(self))

    # @authenticated
    def post(self):
        comp_belong_to = int(self.get_argument("comp_belong_to", -1))
        user_belong_to = int(self.get_argument("user_belong_to", -1))
        comp_status = int(self.get_argument("comp_status", -1))
        comp_belong_to = None if comp_belong_to < 0 else comp_belong_to
        user_belong_to = None if user_belong_to < 0 else user_belong_to
        comp_status = None if comp_status < 0 else comp_status
        weblog.info("%s.%d %d %d", self._request_summary(), comp_belong_to, user_belong_to, comp_status)
        # return self.render('bug/compmtlist.html', bugs=get_compmt_list(self,user_belong_to, comp_belong_to,
        # comp_status), users=get_user_list(self), projects=get_project_list(self))
        bugs = get_compmt_list(self, user_belong_to, comp_belong_to, comp_status)
        compmt_list = gene_compmt_result(self, bugs)
        # for bug in bugs:
        #     print("--", json.dumps(bug, cls=new_alchemy_encoder(), check_circular=False))
        #     compmt_list.append(bug)
        # print(json.dumps(compmt_list))
        # print(compmt_list[0])
        return self.write(json.dumps(compmt_list))


class BugCompmtAddHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        return self.render('bug/compmtadd.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        user_belong_to = int(self.get_argument("user_belong_to", 0))
        comp_belong_to = int(self.get_argument("comp_belong_to", 0))
        comp_type = int(self.get_argument("comp_type", -1))
        comp_new = self.get_argument("comp_new", None)
        comp_status = int(self.get_argument("comp_status", -1))
        comp_describe = self.get_argument("comp_describe", None)
        comp_reason = self.get_argument("comp_reason", None)
        comp_solution = self.get_argument("comp_solution", None)
        comment = self.get_argument("comp_new", None)

        msg = []
        if user_belong_to <= 0 or comp_belong_to <= 0:
            msg.append(u"模块或负责人获取失败，不能为空")
        if comp_type < 0 or comp_status < 0:
            msg.append(u"维护方式 或 是否解决,不能为空")
        if comp_type == 0 and (comp_new is None or comp_new == ''):
            msg.append(u"新增内容不能为空")
        if comp_type > 1 and (comp_describe is None or comp_describe == ''):
            msg.append(u"问题描述不能为空")

        if msg:
            return self.render('bug/compmtadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        else:
            comp_mt = TblComponentMaintenance()
            comp_mt.comp_describe = comp_describe
            comp_mt.comp_type = comp_type
            comp_mt.comp_new = comp_new
            comp_mt.comp_status = comp_status
            comp_mt.comp_belong_to = comp_belong_to
            comp_mt.comment = comment
            comp_mt.comp_reason = comp_reason
            comp_mt.comp_solution = comp_solution
            comp_mt.modify_time = datetime.now()
            comp_mt.create_time = datetime.now()
            comp_mt.user_belong_to = user_belong_to

            try:
                self.mysqldb().add(comp_mt)
                self.mysqldb().commit()
                return self.redirect('/compmt/list')
            except Exception as e:
                self.mysqldb().rollback()
                msg.append(e)
                return self.render('bug/compmtadd.html', message=msg, users=get_user_list(self),
                                   projects=get_project_list(self))



class BugCompmtEditHandler(BaseHandler):
    @authenticated
    def get(self, cid):
        weblog.info("%s.", self._request_summary())
        return self.render('bug/compmtedit.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self), bug=get_compmt_by_id(self, cid))

    def post(self, cid):
        weblog.info("%s.", self._request_summary())
        user_belong_to = int(self.get_argument("user_belong_to", 0))
        comp_belong_to = int(self.get_argument("comp_belong_to", 0))
        comp_type = int(self.get_argument("comp_type", -1))
        comp_new = self.get_argument("comp_new", None)
        comp_status = int(self.get_argument("comp_status", -1))
        comp_describe = self.get_argument("comp_describe", None)
        comp_reason = self.get_argument("comp_reason", None)
        comp_solution = self.get_argument("comp_solution", None)
        comment = self.get_argument("comp_new", None)

        msg = []
        if user_belong_to <= 0 or comp_belong_to <= 0:
            msg.append(u"模块或负责人获取失败，不能为空")
        if comp_type < 0 or comp_status < 0:
            msg.append(u"维护方式 或 是否解决,不能为空")
        if comp_type == 0 and (comp_new is None or comp_new == ''):
            msg.append(u"新增内容不能为空")
        if comp_type > 1 and (comp_describe is None or comp_describe == ''):
            msg.append(u"问题描述不能为空")
        comp_mt = self.mysqldb().query(TblComponentMaintenance).filter(
            TblComponentMaintenance.comp_id == cid).first()
        if comp_mt is None:
            msg.append(u"维护记录不存在, 请返回列表页面查看，record id={}".format(cid))

        if msg:
            return self.render('bug/compmtedit.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        else:
            comp_mt.comp_describe = comp_describe
            comp_mt.comp_type = comp_type
            comp_mt.comp_new = comp_new
            comp_mt.comp_status = comp_status
            comp_mt.comp_belong_to = comp_belong_to
            comp_mt.comment = comment
            comp_mt.comp_reason = comp_reason
            comp_mt.comp_solution = comp_solution
            comp_mt.modify_time = datetime.now()
            comp_mt.create_time = datetime.now()
            comp_mt.user_belong_to = user_belong_to

            try:
                self.mysqldb().commit()
                return self.redirect('/compmt/list')
            except Exception as e:
                self.mysqldb().rollback()
                msg.append(e)
                return self.render('bug/compmtedit.html', message=msg, users=get_user_list(self),
                                   projects=get_project_list(self))


class BugCompmtDeleteHandler(BaseHandler):
    @authenticated
    def get(self, cid):
        weblog.info("%s.", self._request_summary())
        comp_mt = self.mysqldb().query(TblComponentMaintenance).filter_by(comp_id=cid).first()
        comp_mt.comp_status = -1
        try:
            self.mysqldb().commit()
        except Exception as e:
            weblog.error("delete component maintenance id={} error. {}".format(cid, e))
            self.mysqldb().rollback()
        return self.render('bug/compmtlist.html', bugs=get_compmt_list(self),
                           users=get_user_list(self), projects=get_project_list(self))

