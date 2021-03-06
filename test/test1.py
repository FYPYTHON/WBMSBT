# coding=utf-8
# import json
# from database.tbl_project import TblProject
# from database.tbl_bug_list import TblBugList
# from database.tbl_account import TblAccount
# from database.tbl_bug_track import TblBugTrack
# from database.tbl_project_user import TblPorjectUser
# from handlers.base_handler import BaseHandler
# from tornado.web import authenticated
# from tornado.log import access_log as weblog
# from message import msg_define
# from handlers.Email.email_smtp_handler import check_email, check_passord
# from handlers.user_manage_handler import get_user_list, get_user_by_id
# from handlers.Project.project_manage_handler import get_project_list, get_project_by_id
#
#
# def get_bugtrack_list(self, belongid=None, compid=None, level=None):
#     bugs = self.mysqldb().query(TblBugTrack)
#     if belongid is not None:
#         bugs = bugs.filter(TblBugTrack.component_belong == belongid)
#     if compid is not None:
#         bugs = bugs.filter(TblBugTrack.bug_component == compid)
#     if level is not None:
#         bugs = bugs.filter(TblBugTrack.bug_level == level)
#     bugs = bugs.filter(TblBugTrack.bug_project_id > 0)
#     bugs = bugs.order_by(TblBugTrack.bug_date_receive.desc())
#     bugs = bugs.all()
#     # for project in projects:
#     #     print(project.describe,type(project.describe))
#     result = gene_bugtrack_result(self, bugs)
#     return result
#
#
# def get_bugtrack_by_id(self, bug_id):
#     bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bug_id).first()
#     result = gene_bugtrack_result(self, [bug_track])
#     if result:
#         return result[0]
#     else:
#         return []
#
#
# def gene_bugtrack_result(self, bugs):
#     result = []
#     for bug in bugs:
#         bug_dict = dict()
#         bug_dict['bug_id'] = bug.bug_id
#         bug_dict['bug_date_receive'] = str(bug.bug_date_receive)
#         bug_dict['bug_find_by'] = bug.bug_find_by
#         bug_dict['bug_component'] = bug.bug_component
#         bug_dict['component_belong'] = bug.component_belong
#         bug_dict['component_community'] = bug.component_community
#         bug_dict['bug_project_id'] = bug.bug_project_id
#         bug_dict['project_version'] = bug.project_version
#         bug_dict['bug_describe'] = bug.bug_describe
#         bug_dict['bug_level'] = msg_define.BUG_LEVEL[bug.bug_level]
#         bug_dict['bug_reason'] = bug.bug_reason
#         bug_dict['bug_solution'] = bug.bug_solution
#         bug_dict['bug_progress'] = bug.bug_progress
#         bug_dict['bug_date_plan'] = str(bug.bug_date_plan)
#         bug_dict['bug_date_done'] = str(bug.bug_date_done)
#         bug_dict['bug_user_done'] = bug.bug_user_done
#         bug_dict['bug_version'] = bug.bug_version
#         user = get_user_by_id(self, bug.bug_user_done)
#         if user is not None:
#             bug_dict['bug_user_done'] = user.username
#         user_comp_belong = get_user_by_id(self, bug.component_belong)
#         if user_comp_belong is not None:
#             bug_dict['component_belong'] = user_comp_belong.username
#         user_find_by = get_user_by_id(self, bug.bug_find_by)
#         if user_find_by is not None:
#             bug_dict['bug_find_by'] = user_find_by.username
#         project_name = get_project_by_id(self, bug.bug_project_id)
#         if project_name is not None:
#             bug_dict['bug_project_id'] = project_name.project_name
#         comp_name = get_project_by_id(self, bug.bug_component)
#         if comp_name is not None:
#             bug_dict['bug_component'] = comp_name.project_name
#         result.append(bug_dict)
#     return result
#
#
# class BugTrackHandler(BaseHandler):
#     @authenticated
#     def get(self):
#         belongid = self.get_argument("belongid", None)
#         compid = self.get_argument("compid", None)
#         blevel = self.get_argument("blevel", None)
#         weblog.info("%s.", self._request_summary())
#         return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid, blevel),
#                            users=get_user_list(self), projects=get_project_list(self))
#         # return self.render('bug/bugtracklist.html', message="", users=get_user_list(self)
#         #                    , projects=get_project_list(self), bugs=get_bugtrack_list(self))
#
#     @authenticated
#     def post(self):
#         weblog.info("%s.", self._request_summary())
#         bug_component = int(self.get_argument("bug_component", '-1'))
#         component_belong = int(self.get_argument("component_belong", '-1'))
#         bug_level = int(self.get_argument("bug_level", '-1'))
#         bug_component = None if bug_component < 0 else bug_component
#         component_belong = None if component_belong < 0 else component_belong
#         bug_level = None if bug_level < 0 else bug_level
#         bugtracks = get_bugtrack_list(self, component_belong, bug_component, bug_level)
#         weblog.info("%s. %d %d %d", self._request_summary(), bug_component, component_belong, bug_level)
#
#         return self.write(json.dumps(bugtracks))
#
#
# class BugTrackAddHandler(BaseHandler):
#     @authenticated
#     def get(self):
#         weblog.info("%s.", self._request_summary())
#         # return self.render('bug/bugtrackadd.html')
#         return self.render('bug/bugtrackadd.html', message="", users=get_user_list(self)
#                            , projects=get_project_list(self))
#
#     @authenticated
#     def post(self):
#         weblog.info("%s.", self._request_summary())
#         bug_date_receive = self.get_argument("bug_date_receive", None)
#         bug_find_by = int(self.get_argument("bug_find_by", 0))
#         bug_component = int(self.get_argument("bug_component", 0))
#         component_belong = int(self.get_argument("component_belong", 0))
#         component_community = self.get_argument("component_community", None)
#         bug_project_id = int(self.get_argument("bug_project_id", 0))
#         # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
#         project_version = self.get_argument("project_version", None)
#         bug_describe = self.get_argument("bug_describe", None)
#         bug_level = int(self.get_argument("bug_level", 0))
#         bug_reason = self.get_argument("bug_reason", None)
#         bug_solution = self.get_argument("bug_solution", None)
#         bug_progress = self.get_argument("bug_progress", None)
#         bug_date_plan = self.get_argument("bug_date_plan", None)
#         bug_date_done = self.get_argument("bug_date_done", None)
#         bug_user_done = int(self.get_argument("bug_user_done", 0))
#         bug_version = self.get_argument("bug_version", None)
#         msg = []
#         if bug_date_receive is None:
#             msg.append(u"接收日期不能为空")
#         if project_version is None:
#             msg.append(u"模块所属版本不能为空")
#         if bug_date_plan is None or bug_date_done is None:
#             msg.append(u"计划日期或解决日期不能为空")
#         if bug_version is None:
#             msg.append(u"合入版本不能为空")
#         if msg:
#             return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
#                                projects=get_project_list(self))
#         bug_track = TblBugTrack()
#         bug_track.bug_date_receive = bug_date_receive
#         bug_track.bug_find_by = bug_find_by
#         bug_track.bug_component = bug_component
#         bug_track.component_belong = component_belong
#         bug_track.component_community = component_community
#         bug_track.bug_project_id = bug_project_id
#         bug_track.project_version = project_version
#         bug_track.bug_describe = bug_describe
#         bug_track.bug_level = bug_level
#         bug_track.bug_reason = bug_reason
#         bug_track.bug_solution = bug_solution
#         bug_track.bug_progress = bug_progress
#         bug_track.bug_date_plan = bug_date_plan
#         bug_track.bug_date_done = bug_date_done
#         bug_track.bug_user_done = bug_user_done
#         bug_track.bug_version = bug_version
#
#         try:
#             self.mysqldb().add(bug_track)
#             self.mysqldb().commit()
#             return self.redirect("/bugtrack/list")
#         except Exception as e:
#             msg.append(e)
#             return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
#                                projects=get_project_list(self))
#
#
# class BugTrackEditHandler(BaseHandler):
#     @authenticated
#     def get(self, bid):
#         weblog.info("%s.", self._request_summary())
#         # return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid))
#         return self.render('bug/bugtrackedit.html', message="", users=get_user_list(self)
#                            , projects=get_project_list(self), bug=get_bugtrack_by_id(self, bid))
#
#     @authenticated
#     def post(self, bid):
#         weblog.info("%s.", self._request_summary())
#         weblog.info("%s.", self._request_summary())
#         bug_date_receive = self.get_argument("bug_date_receive", None)
#         bug_find_by = int(self.get_argument("bug_find_by", 0))
#         bug_component = int(self.get_argument("bug_component", 0))
#         component_belong = int(self.get_argument("component_belong", 0))
#         component_community = self.get_argument("component_community", None)
#         bug_project_id = int(self.get_argument("bug_project_id", 0))
#         # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
#         project_version = self.get_argument("project_version", None)
#         bug_describe = self.get_argument("bug_describe", None)
#         bug_level = int(self.get_argument("bug_level", 0))
#         bug_reason = self.get_argument("bug_reason", None)
#         bug_solution = self.get_argument("bug_solution", None)
#         bug_progress = self.get_argument("bug_progress", None)
#         bug_date_plan = self.get_argument("bug_date_plan", None)
#         bug_date_done = self.get_argument("bug_date_done", None)
#         bug_user_done = int(self.get_argument("bug_user_done", 0))
#         bug_version = self.get_argument("bug_version", None)
#         msg = []
#         if bug_date_receive is None:
#             msg.append(u"接收日期不能为空")
#         if project_version is None:
#             msg.append(u"模块所属版本不能为空")
#         if bug_date_plan is None or bug_date_done is None:
#             msg.append(u"计划日期或解决日期不能为空")
#         if bug_version is None:
#             msg.append(u"合入版本不能为空")
#         bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bid).first()
#         if bug_track is None:
#             msg.append(u"获取问题单为空，问题单id={}".format(bid))
#         if msg:
#             return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
#                                projects=get_project_list(self))
#         bug_track.bug_date_receive = bug_date_receive
#         bug_track.bug_find_by = bug_find_by
#         bug_track.bug_component = bug_component
#         bug_track.component_belong = component_belong
#         bug_track.component_community = component_community
#         bug_track.bug_project_id = bug_project_id
#         bug_track.project_version = project_version
#         bug_track.bug_describe = bug_describe
#         bug_track.bug_level = bug_level
#         bug_track.bug_reason = bug_reason
#         bug_track.bug_solution = bug_solution
#         bug_track.bug_progress = bug_progress
#         bug_track.bug_date_plan = bug_date_plan
#         bug_track.bug_date_done = bug_date_done
#         bug_track.bug_user_done = bug_user_done
#         bug_track.bug_version = bug_version
#
#         try:
#             self.mysqldb().commit()
#             return self.redirect("/bugtrack/list")
#         except Exception as e:
#             msg.append(e)
#             return self.render('bug/bugtrackedit.html', message=msg, users=get_user_list(self),
#                                projects=get_project_list(self))
#
#
# class BugTrackDeleteHandler(BaseHandler):
#     @authenticated
#     def get(self, bid):
#         weblog.info("%s.", self._request_summary())
#         bug_track = self.mysqldb().query(TblBugTrack).filter_by(comp_id=bid).first()
#         bug_track.bug_project_id = -1
#         try:
#             self.mysqldb().commit()
#         except Exception as e:
#             weblog.error("delete bug track id={} error. {}".format(bid, e))
#             self.mysqldb().rollback()
#
#         return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self))
#
#     @authenticated
#     def post(self):
#         weblog.info("%s.", self._request_summary())

"""
# coding=utf-8
import json
from database.tbl_project import TblProject
from database.tbl_bug_list import TblBugList
from database.tbl_account import TblAccount
from database.tbl_bug_track import TblBugTrack
from database.tbl_project_user import TblPorjectUser
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
from tornado.log import access_log as weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord
from handlers.user_manage_handler import get_user_list, get_user_by_id
from handlers.Project.project_manage_handler import get_project_list, get_project_by_id


def get_bugtrack_list(self, belongid=None, compid=None, level=None):
    bugs = self.mysqldb().query(TblBugTrack)
    if belongid is not None:
        bugs = bugs.filter(TblBugTrack.component_belong == belongid)
    if compid is not None:
        bugs = bugs.filter(TblBugTrack.bug_component == compid)
    if level is not None:
        bugs = bugs.filter(TblBugTrack.bug_level == level)
    bugs = bugs.filter(TblBugTrack.bug_project_id > 0)
    bugs = bugs.order_by(TblBugTrack.bug_date_receive.desc())
    bugs = bugs.all()
    # for project in projects:
    #     print(project.describe,type(project.describe))
    result = gene_bugtrack_result(self, bugs)
    return result


def get_bugtrack_by_id(self, bug_id):
    bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bug_id).first()
    result = gene_bugtrack_result(self, [bug_track])
    if result:
        return result[0]
    else:
        return []


def gene_bugtrack_result(self, bugs):
    result = []
    for bug in bugs:
        bug_dict = dict()
        bug_dict['bug_id'] = bug.bug_id
        bug_dict['bug_date_receive'] = str(bug.bug_date_receive)
        bug_dict['bug_find_by'] = bug.bug_find_by
        bug_dict['bug_component'] = bug.bug_component
        bug_dict['component_belong'] = bug.component_belong
        bug_dict['component_community'] = bug.component_community
        bug_dict['bug_project_id'] = bug.bug_project_id
        bug_dict['project_version'] = bug.project_version
        bug_dict['bug_describe'] = bug.bug_describe
        bug_dict['bug_level'] = msg_define.BUG_LEVEL[bug.bug_level]
        bug_dict['bug_reason'] = bug.bug_reason
        bug_dict['bug_solution'] = bug.bug_solution
        bug_dict['bug_progress'] = bug.bug_progress
        bug_dict['bug_date_plan'] = str(bug.bug_date_plan)
        bug_dict['bug_date_done'] = str(bug.bug_date_done)
        bug_dict['bug_user_done'] = bug.bug_user_done
        bug_dict['bug_version'] = bug.bug_version
        user = get_user_by_id(self, bug.bug_user_done)
        if user is not None:
            bug_dict['bug_user_done'] = user.username
        user_comp_belong = get_user_by_id(self, bug.component_belong)
        if user_comp_belong is not None:
            bug_dict['component_belong'] = user_comp_belong.username
        user_find_by = get_user_by_id(self, bug.bug_find_by)
        if user_find_by is not None:
            bug_dict['bug_find_by'] = user_find_by.username
        project_name = get_project_by_id(self, bug.bug_project_id)
        if project_name is not None:
            bug_dict['bug_project_id'] = project_name.project_name
        comp_name = get_project_by_id(self, bug.bug_component)
        if comp_name is not None:
            bug_dict['bug_component'] = comp_name.project_name
        result.append(bug_dict)
    return result


class BugTrackHandler(BaseHandler):
    @authenticated
    def get(self):
        belongid = self.get_argument("belongid", None)
        compid = self.get_argument("compid", None)
        blevel = self.get_argument("blevel", None)
        weblog.info("%s.", self._request_summary())
        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid, blevel),
                           users=get_user_list(self), projects=get_project_list(self))
        # return self.render('bug/bugtracklist.html', message="", users=get_user_list(self)
        #                    , projects=get_project_list(self), bugs=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_component = int(self.get_argument("bug_component", '-1'))
        component_belong = int(self.get_argument("component_belong", '-1'))
        bug_level = int(self.get_argument("bug_level", '-1'))
        bug_component = None if bug_component < 0 else bug_component
        component_belong = None if component_belong < 0 else component_belong
        bug_level = None if bug_level < 0 else bug_level
        bugtracks = get_bugtrack_list(self, component_belong, bug_component, bug_level)
        weblog.info("%s. %d %d %d", self._request_summary(), bug_component, component_belong, bug_level)

        return self.write(json.dumps(bugtracks))


class BugTrackAddHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtrackadd.html')
        return self.render('bug/bugtrackadd.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track = TblBugTrack()
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().add(bug_track)
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackEditHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid))
        return self.render('bug/bugtrackedit.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self), bug=get_bugtrack_by_id(self, bid))

    @authenticated
    def post(self, bid):
        weblog.info("%s.", self._request_summary())
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bid).first()
        if bug_track is None:
            msg.append(u"获取问题单为空，问题单id={}".format(bid))
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackedit.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackDeleteHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        bug_track = self.mysqldb().query(TblBugTrack).filter_by(comp_id=bid).first()
        bug_track.bug_project_id = -1
        try:
            self.mysqldb().commit()
        except Exception as e:
            weblog.error("delete bug track id={} error. {}".format(bid, e))
            self.mysqldb().rollback()

        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        # coding=utf-8
import json
from database.tbl_project import TblProject
from database.tbl_bug_list import TblBugList
from database.tbl_account import TblAccount
from database.tbl_bug_track import TblBugTrack
from database.tbl_project_user import TblPorjectUser
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
from tornado.log import access_log as weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord
from handlers.user_manage_handler import get_user_list, get_user_by_id
from handlers.Project.project_manage_handler import get_project_list, get_project_by_id


def get_bugtrack_list(self, belongid=None, compid=None, level=None):
    bugs = self.mysqldb().query(TblBugTrack)
    if belongid is not None:
        bugs = bugs.filter(TblBugTrack.component_belong == belongid)
    if compid is not None:
        bugs = bugs.filter(TblBugTrack.bug_component == compid)
    if level is not None:
        bugs = bugs.filter(TblBugTrack.bug_level == level)
    bugs = bugs.filter(TblBugTrack.bug_project_id > 0)
    bugs = bugs.order_by(TblBugTrack.bug_date_receive.desc())
    bugs = bugs.all()
    # for project in projects:
    #     print(project.describe,type(project.describe))
    result = gene_bugtrack_result(self, bugs)
    return result


def get_bugtrack_by_id(self, bug_id):
    bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bug_id).first()
    result = gene_bugtrack_result(self, [bug_track])
    if result:
        return result[0]
    else:
        return []


def gene_bugtrack_result(self, bugs):
    result = []
    for bug in bugs:
        bug_dict = dict()
        bug_dict['bug_id'] = bug.bug_id
        bug_dict['bug_date_receive'] = str(bug.bug_date_receive)
        bug_dict['bug_find_by'] = bug.bug_find_by
        bug_dict['bug_component'] = bug.bug_component
        bug_dict['component_belong'] = bug.component_belong
        bug_dict['component_community'] = bug.component_community
        bug_dict['bug_project_id'] = bug.bug_project_id
        bug_dict['project_version'] = bug.project_version
        bug_dict['bug_describe'] = bug.bug_describe
        bug_dict['bug_level'] = msg_define.BUG_LEVEL[bug.bug_level]
        bug_dict['bug_reason'] = bug.bug_reason
        bug_dict['bug_solution'] = bug.bug_solution
        bug_dict['bug_progress'] = bug.bug_progress
        bug_dict['bug_date_plan'] = str(bug.bug_date_plan)
        bug_dict['bug_date_done'] = str(bug.bug_date_done)
        bug_dict['bug_user_done'] = bug.bug_user_done
        bug_dict['bug_version'] = bug.bug_version
        user = get_user_by_id(self, bug.bug_user_done)
        if user is not None:
            bug_dict['bug_user_done'] = user.username
        user_comp_belong = get_user_by_id(self, bug.component_belong)
        if user_comp_belong is not None:
            bug_dict['component_belong'] = user_comp_belong.username
        user_find_by = get_user_by_id(self, bug.bug_find_by)
        if user_find_by is not None:
            bug_dict['bug_find_by'] = user_find_by.username
        project_name = get_project_by_id(self, bug.bug_project_id)
        if project_name is not None:
            bug_dict['bug_project_id'] = project_name.project_name
        comp_name = get_project_by_id(self, bug.bug_component)
        if comp_name is not None:
            bug_dict['bug_component'] = comp_name.project_name
        result.append(bug_dict)
    return result


class BugTrackHandler(BaseHandler):
    @authenticated
    def get(self):
        belongid = self.get_argument("belongid", None)
        compid = self.get_argument("compid", None)
        blevel = self.get_argument("blevel", None)
        weblog.info("%s.", self._request_summary())
        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid, blevel),
                           users=get_user_list(self), projects=get_project_list(self))
        # return self.render('bug/bugtracklist.html', message="", users=get_user_list(self)
        #                    , projects=get_project_list(self), bugs=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_component = int(self.get_argument("bug_component", '-1'))
        component_belong = int(self.get_argument("component_belong", '-1'))
        bug_level = int(self.get_argument("bug_level", '-1'))
        bug_component = None if bug_component < 0 else bug_component
        component_belong = None if component_belong < 0 else component_belong
        bug_level = None if bug_level < 0 else bug_level
        bugtracks = get_bugtrack_list(self, component_belong, bug_component, bug_level)
        weblog.info("%s. %d %d %d", self._request_summary(), bug_component, component_belong, bug_level)

        return self.write(json.dumps(bugtracks))


class BugTrackAddHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtrackadd.html')
        return self.render('bug/bugtrackadd.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track = TblBugTrack()
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().add(bug_track)
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackEditHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid))
        return self.render('bug/bugtrackedit.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self), bug=get_bugtrack_by_id(self, bid))

    @authenticated
    def post(self, bid):
        weblog.info("%s.", self._request_summary())
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bid).first()
        if bug_track is None:
            msg.append(u"获取问题单为空，问题单id={}".format(bid))
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackedit.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackDeleteHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        bug_track = self.mysqldb().query(TblBugTrack).filter_by(comp_id=bid).first()
        bug_track.bug_project_id = -1
        try:
            self.mysqldb().commit()
        except Exception as e:
            weblog.error("delete bug track id={} error. {}".format(bid, e))
            self.mysqldb().rollback()

        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        # coding=utf-8
import json
from database.tbl_project import TblProject
from database.tbl_bug_list import TblBugList
from database.tbl_account import TblAccount
from database.tbl_bug_track import TblBugTrack
from database.tbl_project_user import TblPorjectUser
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
from tornado.log import access_log as weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord
from handlers.user_manage_handler import get_user_list, get_user_by_id
from handlers.Project.project_manage_handler import get_project_list, get_project_by_id


def get_bugtrack_list(self, belongid=None, compid=None, level=None):
    bugs = self.mysqldb().query(TblBugTrack)
    if belongid is not None:
        bugs = bugs.filter(TblBugTrack.component_belong == belongid)
    if compid is not None:
        bugs = bugs.filter(TblBugTrack.bug_component == compid)
    if level is not None:
        bugs = bugs.filter(TblBugTrack.bug_level == level)
    bugs = bugs.filter(TblBugTrack.bug_project_id > 0)
    bugs = bugs.order_by(TblBugTrack.bug_date_receive.desc())
    bugs = bugs.all()
    # for project in projects:
    #     print(project.describe,type(project.describe))
    result = gene_bugtrack_result(self, bugs)
    return result


def get_bugtrack_by_id(self, bug_id):
    bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bug_id).first()
    result = gene_bugtrack_result(self, [bug_track])
    if result:
        return result[0]
    else:
        return []


def gene_bugtrack_result(self, bugs):
    result = []
    for bug in bugs:
        bug_dict = dict()
        bug_dict['bug_id'] = bug.bug_id
        bug_dict['bug_date_receive'] = str(bug.bug_date_receive)
        bug_dict['bug_find_by'] = bug.bug_find_by
        bug_dict['bug_component'] = bug.bug_component
        bug_dict['component_belong'] = bug.component_belong
        bug_dict['component_community'] = bug.component_community
        bug_dict['bug_project_id'] = bug.bug_project_id
        bug_dict['project_version'] = bug.project_version
        bug_dict['bug_describe'] = bug.bug_describe
        bug_dict['bug_level'] = msg_define.BUG_LEVEL[bug.bug_level]
        bug_dict['bug_reason'] = bug.bug_reason
        bug_dict['bug_solution'] = bug.bug_solution
        bug_dict['bug_progress'] = bug.bug_progress
        bug_dict['bug_date_plan'] = str(bug.bug_date_plan)
        bug_dict['bug_date_done'] = str(bug.bug_date_done)
        bug_dict['bug_user_done'] = bug.bug_user_done
        bug_dict['bug_version'] = bug.bug_version
        user = get_user_by_id(self, bug.bug_user_done)
        if user is not None:
            bug_dict['bug_user_done'] = user.username
        user_comp_belong = get_user_by_id(self, bug.component_belong)
        if user_comp_belong is not None:
            bug_dict['component_belong'] = user_comp_belong.username
        user_find_by = get_user_by_id(self, bug.bug_find_by)
        if user_find_by is not None:
            bug_dict['bug_find_by'] = user_find_by.username
        project_name = get_project_by_id(self, bug.bug_project_id)
        if project_name is not None:
            bug_dict['bug_project_id'] = project_name.project_name
        comp_name = get_project_by_id(self, bug.bug_component)
        if comp_name is not None:
            bug_dict['bug_component'] = comp_name.project_name
        result.append(bug_dict)
    return result


class BugTrackHandler(BaseHandler):
    @authenticated
    def get(self):
        belongid = self.get_argument("belongid", None)
        compid = self.get_argument("compid", None)
        blevel = self.get_argument("blevel", None)
        weblog.info("%s.", self._request_summary())
        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid, blevel),
                           users=get_user_list(self), projects=get_project_list(self))
        # return self.render('bug/bugtracklist.html', message="", users=get_user_list(self)
        #                    , projects=get_project_list(self), bugs=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_component = int(self.get_argument("bug_component", '-1'))
        component_belong = int(self.get_argument("component_belong", '-1'))
        bug_level = int(self.get_argument("bug_level", '-1'))
        bug_component = None if bug_component < 0 else bug_component
        component_belong = None if component_belong < 0 else component_belong
        bug_level = None if bug_level < 0 else bug_level
        bugtracks = get_bugtrack_list(self, component_belong, bug_component, bug_level)
        weblog.info("%s. %d %d %d", self._request_summary(), bug_component, component_belong, bug_level)

        return self.write(json.dumps(bugtracks))


class BugTrackAddHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtrackadd.html')
        return self.render('bug/bugtrackadd.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track = TblBugTrack()
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().add(bug_track)
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackEditHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid))
        return self.render('bug/bugtrackedit.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self), bug=get_bugtrack_by_id(self, bid))

    @authenticated
    def post(self, bid):
        weblog.info("%s.", self._request_summary())
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bid).first()
        if bug_track is None:
            msg.append(u"获取问题单为空，问题单id={}".format(bid))
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackedit.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackDeleteHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        bug_track = self.mysqldb().query(TblBugTrack).filter_by(comp_id=bid).first()
        bug_track.bug_project_id = -1
        try:
            self.mysqldb().commit()
        except Exception as e:
            weblog.error("delete bug track id={} error. {}".format(bid, e))
            self.mysqldb().rollback()

        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        # coding=utf-8
import json
from database.tbl_project import TblProject
from database.tbl_bug_list import TblBugList
from database.tbl_account import TblAccount
from database.tbl_bug_track import TblBugTrack
from database.tbl_project_user import TblPorjectUser
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
from tornado.log import access_log as weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord
from handlers.user_manage_handler import get_user_list, get_user_by_id
from handlers.Project.project_manage_handler import get_project_list, get_project_by_id


def get_bugtrack_list(self, belongid=None, compid=None, level=None):
    bugs = self.mysqldb().query(TblBugTrack)
    if belongid is not None:
        bugs = bugs.filter(TblBugTrack.component_belong == belongid)
    if compid is not None:
        bugs = bugs.filter(TblBugTrack.bug_component == compid)
    if level is not None:
        bugs = bugs.filter(TblBugTrack.bug_level == level)
    bugs = bugs.filter(TblBugTrack.bug_project_id > 0)
    bugs = bugs.order_by(TblBugTrack.bug_date_receive.desc())
    bugs = bugs.all()
    # for project in projects:
    #     print(project.describe,type(project.describe))
    result = gene_bugtrack_result(self, bugs)
    return result


def get_bugtrack_by_id(self, bug_id):
    bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bug_id).first()
    result = gene_bugtrack_result(self, [bug_track])
    if result:
        return result[0]
    else:
        return []


def gene_bugtrack_result(self, bugs):
    result = []
    for bug in bugs:
        bug_dict = dict()
        bug_dict['bug_id'] = bug.bug_id
        bug_dict['bug_date_receive'] = str(bug.bug_date_receive)
        bug_dict['bug_find_by'] = bug.bug_find_by
        bug_dict['bug_component'] = bug.bug_component
        bug_dict['component_belong'] = bug.component_belong
        bug_dict['component_community'] = bug.component_community
        bug_dict['bug_project_id'] = bug.bug_project_id
        bug_dict['project_version'] = bug.project_version
        bug_dict['bug_describe'] = bug.bug_describe
        bug_dict['bug_level'] = msg_define.BUG_LEVEL[bug.bug_level]
        bug_dict['bug_reason'] = bug.bug_reason
        bug_dict['bug_solution'] = bug.bug_solution
        bug_dict['bug_progress'] = bug.bug_progress
        bug_dict['bug_date_plan'] = str(bug.bug_date_plan)
        bug_dict['bug_date_done'] = str(bug.bug_date_done)
        bug_dict['bug_user_done'] = bug.bug_user_done
        bug_dict['bug_version'] = bug.bug_version
        user = get_user_by_id(self, bug.bug_user_done)
        if user is not None:
            bug_dict['bug_user_done'] = user.username
        user_comp_belong = get_user_by_id(self, bug.component_belong)
        if user_comp_belong is not None:
            bug_dict['component_belong'] = user_comp_belong.username
        user_find_by = get_user_by_id(self, bug.bug_find_by)
        if user_find_by is not None:
            bug_dict['bug_find_by'] = user_find_by.username
        project_name = get_project_by_id(self, bug.bug_project_id)
        if project_name is not None:
            bug_dict['bug_project_id'] = project_name.project_name
        comp_name = get_project_by_id(self, bug.bug_component)
        if comp_name is not None:
            bug_dict['bug_component'] = comp_name.project_name
        result.append(bug_dict)
    return result


class BugTrackHandler(BaseHandler):
    @authenticated
    def get(self):
        belongid = self.get_argument("belongid", None)
        compid = self.get_argument("compid", None)
        blevel = self.get_argument("blevel", None)
        weblog.info("%s.", self._request_summary())
        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid, blevel),
                           users=get_user_list(self), projects=get_project_list(self))
        # return self.render('bug/bugtracklist.html', message="", users=get_user_list(self)
        #                    , projects=get_project_list(self), bugs=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_component = int(self.get_argument("bug_component", '-1'))
        component_belong = int(self.get_argument("component_belong", '-1'))
        bug_level = int(self.get_argument("bug_level", '-1'))
        bug_component = None if bug_component < 0 else bug_component
        component_belong = None if component_belong < 0 else component_belong
        bug_level = None if bug_level < 0 else bug_level
        bugtracks = get_bugtrack_list(self, component_belong, bug_component, bug_level)
        weblog.info("%s. %d %d %d", self._request_summary(), bug_component, component_belong, bug_level)

        return self.write(json.dumps(bugtracks))


class BugTrackAddHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtrackadd.html')
        return self.render('bug/bugtrackadd.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track = TblBugTrack()
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().add(bug_track)
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackEditHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid))
        return self.render('bug/bugtrackedit.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self), bug=get_bugtrack_by_id(self, bid))

    @authenticated
    def post(self, bid):
        weblog.info("%s.", self._request_summary())
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bid).first()
        if bug_track is None:
            msg.append(u"获取问题单为空，问题单id={}".format(bid))
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackedit.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackDeleteHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        bug_track = self.mysqldb().query(TblBugTrack).filter_by(comp_id=bid).first()
        bug_track.bug_project_id = -1
        try:
            self.mysqldb().commit()
        except Exception as e:
            weblog.error("delete bug track id={} error. {}".format(bid, e))
            self.mysqldb().rollback()

        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        # coding=utf-8
import json
from database.tbl_project import TblProject
from database.tbl_bug_list import TblBugList
from database.tbl_account import TblAccount
from database.tbl_bug_track import TblBugTrack
from database.tbl_project_user import TblPorjectUser
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
from tornado.log import access_log as weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord
from handlers.user_manage_handler import get_user_list, get_user_by_id
from handlers.Project.project_manage_handler import get_project_list, get_project_by_id


def get_bugtrack_list(self, belongid=None, compid=None, level=None):
    bugs = self.mysqldb().query(TblBugTrack)
    if belongid is not None:
        bugs = bugs.filter(TblBugTrack.component_belong == belongid)
    if compid is not None:
        bugs = bugs.filter(TblBugTrack.bug_component == compid)
    if level is not None:
        bugs = bugs.filter(TblBugTrack.bug_level == level)
    bugs = bugs.filter(TblBugTrack.bug_project_id > 0)
    bugs = bugs.order_by(TblBugTrack.bug_date_receive.desc())
    bugs = bugs.all()
    # for project in projects:
    #     print(project.describe,type(project.describe))
    result = gene_bugtrack_result(self, bugs)
    return result


def get_bugtrack_by_id(self, bug_id):
    bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bug_id).first()
    result = gene_bugtrack_result(self, [bug_track])
    if result:
        return result[0]
    else:
        return []


def gene_bugtrack_result(self, bugs):
    result = []
    for bug in bugs:
        bug_dict = dict()
        bug_dict['bug_id'] = bug.bug_id
        bug_dict['bug_date_receive'] = str(bug.bug_date_receive)
        bug_dict['bug_find_by'] = bug.bug_find_by
        bug_dict['bug_component'] = bug.bug_component
        bug_dict['component_belong'] = bug.component_belong
        bug_dict['component_community'] = bug.component_community
        bug_dict['bug_project_id'] = bug.bug_project_id
        bug_dict['project_version'] = bug.project_version
        bug_dict['bug_describe'] = bug.bug_describe
        bug_dict['bug_level'] = msg_define.BUG_LEVEL[bug.bug_level]
        bug_dict['bug_reason'] = bug.bug_reason
        bug_dict['bug_solution'] = bug.bug_solution
        bug_dict['bug_progress'] = bug.bug_progress
        bug_dict['bug_date_plan'] = str(bug.bug_date_plan)
        bug_dict['bug_date_done'] = str(bug.bug_date_done)
        bug_dict['bug_user_done'] = bug.bug_user_done
        bug_dict['bug_version'] = bug.bug_version
        user = get_user_by_id(self, bug.bug_user_done)
        if user is not None:
            bug_dict['bug_user_done'] = user.username
        user_comp_belong = get_user_by_id(self, bug.component_belong)
        if user_comp_belong is not None:
            bug_dict['component_belong'] = user_comp_belong.username
        user_find_by = get_user_by_id(self, bug.bug_find_by)
        if user_find_by is not None:
            bug_dict['bug_find_by'] = user_find_by.username
        project_name = get_project_by_id(self, bug.bug_project_id)
        if project_name is not None:
            bug_dict['bug_project_id'] = project_name.project_name
        comp_name = get_project_by_id(self, bug.bug_component)
        if comp_name is not None:
            bug_dict['bug_component'] = comp_name.project_name
        result.append(bug_dict)
    return result


class BugTrackHandler(BaseHandler):
    @authenticated
    def get(self):
        belongid = self.get_argument("belongid", None)
        compid = self.get_argument("compid", None)
        blevel = self.get_argument("blevel", None)
        weblog.info("%s.", self._request_summary())
        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid, blevel),
                           users=get_user_list(self), projects=get_project_list(self))
        # return self.render('bug/bugtracklist.html', message="", users=get_user_list(self)
        #                    , projects=get_project_list(self), bugs=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_component = int(self.get_argument("bug_component", '-1'))
        component_belong = int(self.get_argument("component_belong", '-1'))
        bug_level = int(self.get_argument("bug_level", '-1'))
        bug_component = None if bug_component < 0 else bug_component
        component_belong = None if component_belong < 0 else component_belong
        bug_level = None if bug_level < 0 else bug_level
        bugtracks = get_bugtrack_list(self, component_belong, bug_component, bug_level)
        weblog.info("%s. %d %d %d", self._request_summary(), bug_component, component_belong, bug_level)

        return self.write(json.dumps(bugtracks))


class BugTrackAddHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtrackadd.html')
        return self.render('bug/bugtrackadd.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track = TblBugTrack()
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().add(bug_track)
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackEditHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid))
        return self.render('bug/bugtrackedit.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self), bug=get_bugtrack_by_id(self, bid))

    @authenticated
    def post(self, bid):
        weblog.info("%s.", self._request_summary())
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bid).first()
        if bug_track is None:
            msg.append(u"获取问题单为空，问题单id={}".format(bid))
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackedit.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackDeleteHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        bug_track = self.mysqldb().query(TblBugTrack).filter_by(comp_id=bid).first()
        bug_track.bug_project_id = -1
        try:
            self.mysqldb().commit()
        except Exception as e:
            weblog.error("delete bug track id={} error. {}".format(bid, e))
            self.mysqldb().rollback()

        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        # coding=utf-8
import json
from database.tbl_project import TblProject
from database.tbl_bug_list import TblBugList
from database.tbl_account import TblAccount
from database.tbl_bug_track import TblBugTrack
from database.tbl_project_user import TblPorjectUser
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
from tornado.log import access_log as weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord
from handlers.user_manage_handler import get_user_list, get_user_by_id
from handlers.Project.project_manage_handler import get_project_list, get_project_by_id


def get_bugtrack_list(self, belongid=None, compid=None, level=None):
    bugs = self.mysqldb().query(TblBugTrack)
    if belongid is not None:
        bugs = bugs.filter(TblBugTrack.component_belong == belongid)
    if compid is not None:
        bugs = bugs.filter(TblBugTrack.bug_component == compid)
    if level is not None:
        bugs = bugs.filter(TblBugTrack.bug_level == level)
    bugs = bugs.filter(TblBugTrack.bug_project_id > 0)
    bugs = bugs.order_by(TblBugTrack.bug_date_receive.desc())
    bugs = bugs.all()
    # for project in projects:
    #     print(project.describe,type(project.describe))
    result = gene_bugtrack_result(self, bugs)
    return result


def get_bugtrack_by_id(self, bug_id):
    bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bug_id).first()
    result = gene_bugtrack_result(self, [bug_track])
    if result:
        return result[0]
    else:
        return []


def gene_bugtrack_result(self, bugs):
    result = []
    for bug in bugs:
        bug_dict = dict()
        bug_dict['bug_id'] = bug.bug_id
        bug_dict['bug_date_receive'] = str(bug.bug_date_receive)
        bug_dict['bug_find_by'] = bug.bug_find_by
        bug_dict['bug_component'] = bug.bug_component
        bug_dict['component_belong'] = bug.component_belong
        bug_dict['component_community'] = bug.component_community
        bug_dict['bug_project_id'] = bug.bug_project_id
        bug_dict['project_version'] = bug.project_version
        bug_dict['bug_describe'] = bug.bug_describe
        bug_dict['bug_level'] = msg_define.BUG_LEVEL[bug.bug_level]
        bug_dict['bug_reason'] = bug.bug_reason
        bug_dict['bug_solution'] = bug.bug_solution
        bug_dict['bug_progress'] = bug.bug_progress
        bug_dict['bug_date_plan'] = str(bug.bug_date_plan)
        bug_dict['bug_date_done'] = str(bug.bug_date_done)
        bug_dict['bug_user_done'] = bug.bug_user_done
        bug_dict['bug_version'] = bug.bug_version
        user = get_user_by_id(self, bug.bug_user_done)
        if user is not None:
            bug_dict['bug_user_done'] = user.username
        user_comp_belong = get_user_by_id(self, bug.component_belong)
        if user_comp_belong is not None:
            bug_dict['component_belong'] = user_comp_belong.username
        user_find_by = get_user_by_id(self, bug.bug_find_by)
        if user_find_by is not None:
            bug_dict['bug_find_by'] = user_find_by.username
        project_name = get_project_by_id(self, bug.bug_project_id)
        if project_name is not None:
            bug_dict['bug_project_id'] = project_name.project_name
        comp_name = get_project_by_id(self, bug.bug_component)
        if comp_name is not None:
            bug_dict['bug_component'] = comp_name.project_name
        result.append(bug_dict)
    return result


class BugTrackHandler(BaseHandler):
    @authenticated
    def get(self):
        belongid = self.get_argument("belongid", None)
        compid = self.get_argument("compid", None)
        blevel = self.get_argument("blevel", None)
        weblog.info("%s.", self._request_summary())
        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid, blevel),
                           users=get_user_list(self), projects=get_project_list(self))
        # return self.render('bug/bugtracklist.html', message="", users=get_user_list(self)
        #                    , projects=get_project_list(self), bugs=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_component = int(self.get_argument("bug_component", '-1'))
        component_belong = int(self.get_argument("component_belong", '-1'))
        bug_level = int(self.get_argument("bug_level", '-1'))
        bug_component = None if bug_component < 0 else bug_component
        component_belong = None if component_belong < 0 else component_belong
        bug_level = None if bug_level < 0 else bug_level
        bugtracks = get_bugtrack_list(self, component_belong, bug_component, bug_level)
        weblog.info("%s. %d %d %d", self._request_summary(), bug_component, component_belong, bug_level)

        return self.write(json.dumps(bugtracks))


class BugTrackAddHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtrackadd.html')
        return self.render('bug/bugtrackadd.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track = TblBugTrack()
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().add(bug_track)
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackEditHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid))
        return self.render('bug/bugtrackedit.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self), bug=get_bugtrack_by_id(self, bid))

    @authenticated
    def post(self, bid):
        weblog.info("%s.", self._request_summary())
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bid).first()
        if bug_track is None:
            msg.append(u"获取问题单为空，问题单id={}".format(bid))
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackedit.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackDeleteHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        bug_track = self.mysqldb().query(TblBugTrack).filter_by(comp_id=bid).first()
        bug_track.bug_project_id = -1
        try:
            self.mysqldb().commit()
        except Exception as e:
            weblog.error("delete bug track id={} error. {}".format(bid, e))
            self.mysqldb().rollback()

        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        # coding=utf-8
import json
from database.tbl_project import TblProject
from database.tbl_bug_list import TblBugList
from database.tbl_account import TblAccount
from database.tbl_bug_track import TblBugTrack
from database.tbl_project_user import TblPorjectUser
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
from tornado.log import access_log as weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord
from handlers.user_manage_handler import get_user_list, get_user_by_id
from handlers.Project.project_manage_handler import get_project_list, get_project_by_id


def get_bugtrack_list(self, belongid=None, compid=None, level=None):
    bugs = self.mysqldb().query(TblBugTrack)
    if belongid is not None:
        bugs = bugs.filter(TblBugTrack.component_belong == belongid)
    if compid is not None:
        bugs = bugs.filter(TblBugTrack.bug_component == compid)
    if level is not None:
        bugs = bugs.filter(TblBugTrack.bug_level == level)
    bugs = bugs.filter(TblBugTrack.bug_project_id > 0)
    bugs = bugs.order_by(TblBugTrack.bug_date_receive.desc())
    bugs = bugs.all()
    # for project in projects:
    #     print(project.describe,type(project.describe))
    result = gene_bugtrack_result(self, bugs)
    return result


def get_bugtrack_by_id(self, bug_id):
    bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bug_id).first()
    result = gene_bugtrack_result(self, [bug_track])
    if result:
        return result[0]
    else:
        return []


def gene_bugtrack_result(self, bugs):
    result = []
    for bug in bugs:
        bug_dict = dict()
        bug_dict['bug_id'] = bug.bug_id
        bug_dict['bug_date_receive'] = str(bug.bug_date_receive)
        bug_dict['bug_find_by'] = bug.bug_find_by
        bug_dict['bug_component'] = bug.bug_component
        bug_dict['component_belong'] = bug.component_belong
        bug_dict['component_community'] = bug.component_community
        bug_dict['bug_project_id'] = bug.bug_project_id
        bug_dict['project_version'] = bug.project_version
        bug_dict['bug_describe'] = bug.bug_describe
        bug_dict['bug_level'] = msg_define.BUG_LEVEL[bug.bug_level]
        bug_dict['bug_reason'] = bug.bug_reason
        bug_dict['bug_solution'] = bug.bug_solution
        bug_dict['bug_progress'] = bug.bug_progress
        bug_dict['bug_date_plan'] = str(bug.bug_date_plan)
        bug_dict['bug_date_done'] = str(bug.bug_date_done)
        bug_dict['bug_user_done'] = bug.bug_user_done
        bug_dict['bug_version'] = bug.bug_version
        user = get_user_by_id(self, bug.bug_user_done)
        if user is not None:
            bug_dict['bug_user_done'] = user.username
        user_comp_belong = get_user_by_id(self, bug.component_belong)
        if user_comp_belong is not None:
            bug_dict['component_belong'] = user_comp_belong.username
        user_find_by = get_user_by_id(self, bug.bug_find_by)
        if user_find_by is not None:
            bug_dict['bug_find_by'] = user_find_by.username
        project_name = get_project_by_id(self, bug.bug_project_id)
        if project_name is not None:
            bug_dict['bug_project_id'] = project_name.project_name
        comp_name = get_project_by_id(self, bug.bug_component)
        if comp_name is not None:
            bug_dict['bug_component'] = comp_name.project_name
        result.append(bug_dict)
    return result


class BugTrackHandler(BaseHandler):
    @authenticated
    def get(self):
        belongid = self.get_argument("belongid", None)
        compid = self.get_argument("compid", None)
        blevel = self.get_argument("blevel", None)
        weblog.info("%s.", self._request_summary())
        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid, blevel),
                           users=get_user_list(self), projects=get_project_list(self))
        # return self.render('bug/bugtracklist.html', message="", users=get_user_list(self)
        #                    , projects=get_project_list(self), bugs=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_component = int(self.get_argument("bug_component", '-1'))
        component_belong = int(self.get_argument("component_belong", '-1'))
        bug_level = int(self.get_argument("bug_level", '-1'))
        bug_component = None if bug_component < 0 else bug_component
        component_belong = None if component_belong < 0 else component_belong
        bug_level = None if bug_level < 0 else bug_level
        bugtracks = get_bugtrack_list(self, component_belong, bug_component, bug_level)
        weblog.info("%s. %d %d %d", self._request_summary(), bug_component, component_belong, bug_level)

        return self.write(json.dumps(bugtracks))


class BugTrackAddHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtrackadd.html')
        return self.render('bug/bugtrackadd.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track = TblBugTrack()
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().add(bug_track)
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackEditHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid))
        return self.render('bug/bugtrackedit.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self), bug=get_bugtrack_by_id(self, bid))

    @authenticated
    def post(self, bid):
        weblog.info("%s.", self._request_summary())
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bid).first()
        if bug_track is None:
            msg.append(u"获取问题单为空，问题单id={}".format(bid))
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackedit.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackDeleteHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        bug_track = self.mysqldb().query(TblBugTrack).filter_by(comp_id=bid).first()
        bug_track.bug_project_id = -1
        try:
            self.mysqldb().commit()
        except Exception as e:
            weblog.error("delete bug track id={} error. {}".format(bid, e))
            self.mysqldb().rollback()

        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        
        
        # coding=utf-8
import json
from database.tbl_project import TblProject
from database.tbl_bug_list import TblBugList
from database.tbl_account import TblAccount
from database.tbl_bug_track import TblBugTrack
from database.tbl_project_user import TblPorjectUser
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
from tornado.log import access_log as weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord
from handlers.user_manage_handler import get_user_list, get_user_by_id
from handlers.Project.project_manage_handler import get_project_list, get_project_by_id


def get_bugtrack_list(self, belongid=None, compid=None, level=None):
    bugs = self.mysqldb().query(TblBugTrack)
    if belongid is not None:
        bugs = bugs.filter(TblBugTrack.component_belong == belongid)
    if compid is not None:
        bugs = bugs.filter(TblBugTrack.bug_component == compid)
    if level is not None:
        bugs = bugs.filter(TblBugTrack.bug_level == level)
    bugs = bugs.filter(TblBugTrack.bug_project_id > 0)
    bugs = bugs.order_by(TblBugTrack.bug_date_receive.desc())
    bugs = bugs.all()
    # for project in projects:
    #     print(project.describe,type(project.describe))
    result = gene_bugtrack_result(self, bugs)
    return result


def get_bugtrack_by_id(self, bug_id):
    bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bug_id).first()
    result = gene_bugtrack_result(self, [bug_track])
    if result:
        return result[0]
    else:
        return []


def gene_bugtrack_result(self, bugs):
    result = []
    for bug in bugs:
        bug_dict = dict()
        bug_dict['bug_id'] = bug.bug_id
        bug_dict['bug_date_receive'] = str(bug.bug_date_receive)
        bug_dict['bug_find_by'] = bug.bug_find_by
        bug_dict['bug_component'] = bug.bug_component
        bug_dict['component_belong'] = bug.component_belong
        bug_dict['component_community'] = bug.component_community
        bug_dict['bug_project_id'] = bug.bug_project_id
        bug_dict['project_version'] = bug.project_version
        bug_dict['bug_describe'] = bug.bug_describe
        bug_dict['bug_level'] = msg_define.BUG_LEVEL[bug.bug_level]
        bug_dict['bug_reason'] = bug.bug_reason
        bug_dict['bug_solution'] = bug.bug_solution
        bug_dict['bug_progress'] = bug.bug_progress
        bug_dict['bug_date_plan'] = str(bug.bug_date_plan)
        bug_dict['bug_date_done'] = str(bug.bug_date_done)
        bug_dict['bug_user_done'] = bug.bug_user_done
        bug_dict['bug_version'] = bug.bug_version
        user = get_user_by_id(self, bug.bug_user_done)
        if user is not None:
            bug_dict['bug_user_done'] = user.username
        user_comp_belong = get_user_by_id(self, bug.component_belong)
        if user_comp_belong is not None:
            bug_dict['component_belong'] = user_comp_belong.username
        user_find_by = get_user_by_id(self, bug.bug_find_by)
        if user_find_by is not None:
            bug_dict['bug_find_by'] = user_find_by.username
        project_name = get_project_by_id(self, bug.bug_project_id)
        if project_name is not None:
            bug_dict['bug_project_id'] = project_name.project_name
        comp_name = get_project_by_id(self, bug.bug_component)
        if comp_name is not None:
            bug_dict['bug_component'] = comp_name.project_name
        result.append(bug_dict)
    return result


class BugTrackHandler(BaseHandler):
    @authenticated
    def get(self):
        belongid = self.get_argument("belongid", None)
        compid = self.get_argument("compid", None)
        blevel = self.get_argument("blevel", None)
        weblog.info("%s.", self._request_summary())
        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid, blevel),
                           users=get_user_list(self), projects=get_project_list(self))
        # return self.render('bug/bugtracklist.html', message="", users=get_user_list(self)
        #                    , projects=get_project_list(self), bugs=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_component = int(self.get_argument("bug_component", '-1'))
        component_belong = int(self.get_argument("component_belong", '-1'))
        bug_level = int(self.get_argument("bug_level", '-1'))
        bug_component = None if bug_component < 0 else bug_component
        component_belong = None if component_belong < 0 else component_belong
        bug_level = None if bug_level < 0 else bug_level
        bugtracks = get_bugtrack_list(self, component_belong, bug_component, bug_level)
        weblog.info("%s. %d %d %d", self._request_summary(), bug_component, component_belong, bug_level)

        return self.write(json.dumps(bugtracks))


class BugTrackAddHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtrackadd.html')
        return self.render('bug/bugtrackadd.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track = TblBugTrack()
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().add(bug_track)
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackEditHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid))
        return self.render('bug/bugtrackedit.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self), bug=get_bugtrack_by_id(self, bid))

    @authenticated
    def post(self, bid):
        weblog.info("%s.", self._request_summary())
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bid).first()
        if bug_track is None:
            msg.append(u"获取问题单为空，问题单id={}".format(bid))
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackedit.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackDeleteHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        bug_track = self.mysqldb().query(TblBugTrack).filter_by(comp_id=bid).first()
        bug_track.bug_project_id = -1
        try:
            self.mysqldb().commit()
        except Exception as e:
            weblog.error("delete bug track id={} error. {}".format(bid, e))
            self.mysqldb().rollback()

        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        # coding=utf-8
import json
from database.tbl_project import TblProject
from database.tbl_bug_list import TblBugList
from database.tbl_account import TblAccount
from database.tbl_bug_track import TblBugTrack
from database.tbl_project_user import TblPorjectUser
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
from tornado.log import access_log as weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord
from handlers.user_manage_handler import get_user_list, get_user_by_id
from handlers.Project.project_manage_handler import get_project_list, get_project_by_id


def get_bugtrack_list(self, belongid=None, compid=None, level=None):
    bugs = self.mysqldb().query(TblBugTrack)
    if belongid is not None:
        bugs = bugs.filter(TblBugTrack.component_belong == belongid)
    if compid is not None:
        bugs = bugs.filter(TblBugTrack.bug_component == compid)
    if level is not None:
        bugs = bugs.filter(TblBugTrack.bug_level == level)
    bugs = bugs.filter(TblBugTrack.bug_project_id > 0)
    bugs = bugs.order_by(TblBugTrack.bug_date_receive.desc())
    bugs = bugs.all()
    # for project in projects:
    #     print(project.describe,type(project.describe))
    result = gene_bugtrack_result(self, bugs)
    return result


def get_bugtrack_by_id(self, bug_id):
    bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bug_id).first()
    result = gene_bugtrack_result(self, [bug_track])
    if result:
        return result[0]
    else:
        return []


def gene_bugtrack_result(self, bugs):
    result = []
    for bug in bugs:
        bug_dict = dict()
        bug_dict['bug_id'] = bug.bug_id
        bug_dict['bug_date_receive'] = str(bug.bug_date_receive)
        bug_dict['bug_find_by'] = bug.bug_find_by
        bug_dict['bug_component'] = bug.bug_component
        bug_dict['component_belong'] = bug.component_belong
        bug_dict['component_community'] = bug.component_community
        bug_dict['bug_project_id'] = bug.bug_project_id
        bug_dict['project_version'] = bug.project_version
        bug_dict['bug_describe'] = bug.bug_describe
        bug_dict['bug_level'] = msg_define.BUG_LEVEL[bug.bug_level]
        bug_dict['bug_reason'] = bug.bug_reason
        bug_dict['bug_solution'] = bug.bug_solution
        bug_dict['bug_progress'] = bug.bug_progress
        bug_dict['bug_date_plan'] = str(bug.bug_date_plan)
        bug_dict['bug_date_done'] = str(bug.bug_date_done)
        bug_dict['bug_user_done'] = bug.bug_user_done
        bug_dict['bug_version'] = bug.bug_version
        user = get_user_by_id(self, bug.bug_user_done)
        if user is not None:
            bug_dict['bug_user_done'] = user.username
        user_comp_belong = get_user_by_id(self, bug.component_belong)
        if user_comp_belong is not None:
            bug_dict['component_belong'] = user_comp_belong.username
        user_find_by = get_user_by_id(self, bug.bug_find_by)
        if user_find_by is not None:
            bug_dict['bug_find_by'] = user_find_by.username
        project_name = get_project_by_id(self, bug.bug_project_id)
        if project_name is not None:
            bug_dict['bug_project_id'] = project_name.project_name
        comp_name = get_project_by_id(self, bug.bug_component)
        if comp_name is not None:
            bug_dict['bug_component'] = comp_name.project_name
        result.append(bug_dict)
    return result


class BugTrackHandler(BaseHandler):
    @authenticated
    def get(self):
        belongid = self.get_argument("belongid", None)
        compid = self.get_argument("compid", None)
        blevel = self.get_argument("blevel", None)
        weblog.info("%s.", self._request_summary())
        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid, blevel),
                           users=get_user_list(self), projects=get_project_list(self))
        # return self.render('bug/bugtracklist.html', message="", users=get_user_list(self)
        #                    , projects=get_project_list(self), bugs=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_component = int(self.get_argument("bug_component", '-1'))
        component_belong = int(self.get_argument("component_belong", '-1'))
        bug_level = int(self.get_argument("bug_level", '-1'))
        bug_component = None if bug_component < 0 else bug_component
        component_belong = None if component_belong < 0 else component_belong
        bug_level = None if bug_level < 0 else bug_level
        bugtracks = get_bugtrack_list(self, component_belong, bug_component, bug_level)
        weblog.info("%s. %d %d %d", self._request_summary(), bug_component, component_belong, bug_level)

        return self.write(json.dumps(bugtracks))


class BugTrackAddHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtrackadd.html')
        return self.render('bug/bugtrackadd.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track = TblBugTrack()
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().add(bug_track)
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackEditHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid))
        return self.render('bug/bugtrackedit.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self), bug=get_bugtrack_by_id(self, bid))

    @authenticated
    def post(self, bid):
        weblog.info("%s.", self._request_summary())
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bid).first()
        if bug_track is None:
            msg.append(u"获取问题单为空，问题单id={}".format(bid))
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackedit.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackDeleteHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        bug_track = self.mysqldb().query(TblBugTrack).filter_by(comp_id=bid).first()
        bug_track.bug_project_id = -1
        try:
            self.mysqldb().commit()
        except Exception as e:
            weblog.error("delete bug track id={} error. {}".format(bid, e))
            self.mysqldb().rollback()

        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        # coding=utf-8
import json
from database.tbl_project import TblProject
from database.tbl_bug_list import TblBugList
from database.tbl_account import TblAccount
from database.tbl_bug_track import TblBugTrack
from database.tbl_project_user import TblPorjectUser
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
from tornado.log import access_log as weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord
from handlers.user_manage_handler import get_user_list, get_user_by_id
from handlers.Project.project_manage_handler import get_project_list, get_project_by_id


def get_bugtrack_list(self, belongid=None, compid=None, level=None):
    bugs = self.mysqldb().query(TblBugTrack)
    if belongid is not None:
        bugs = bugs.filter(TblBugTrack.component_belong == belongid)
    if compid is not None:
        bugs = bugs.filter(TblBugTrack.bug_component == compid)
    if level is not None:
        bugs = bugs.filter(TblBugTrack.bug_level == level)
    bugs = bugs.filter(TblBugTrack.bug_project_id > 0)
    bugs = bugs.order_by(TblBugTrack.bug_date_receive.desc())
    bugs = bugs.all()
    # for project in projects:
    #     print(project.describe,type(project.describe))
    result = gene_bugtrack_result(self, bugs)
    return result


def get_bugtrack_by_id(self, bug_id):
    bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bug_id).first()
    result = gene_bugtrack_result(self, [bug_track])
    if result:
        return result[0]
    else:
        return []


def gene_bugtrack_result(self, bugs):
    result = []
    for bug in bugs:
        bug_dict = dict()
        bug_dict['bug_id'] = bug.bug_id
        bug_dict['bug_date_receive'] = str(bug.bug_date_receive)
        bug_dict['bug_find_by'] = bug.bug_find_by
        bug_dict['bug_component'] = bug.bug_component
        bug_dict['component_belong'] = bug.component_belong
        bug_dict['component_community'] = bug.component_community
        bug_dict['bug_project_id'] = bug.bug_project_id
        bug_dict['project_version'] = bug.project_version
        bug_dict['bug_describe'] = bug.bug_describe
        bug_dict['bug_level'] = msg_define.BUG_LEVEL[bug.bug_level]
        bug_dict['bug_reason'] = bug.bug_reason
        bug_dict['bug_solution'] = bug.bug_solution
        bug_dict['bug_progress'] = bug.bug_progress
        bug_dict['bug_date_plan'] = str(bug.bug_date_plan)
        bug_dict['bug_date_done'] = str(bug.bug_date_done)
        bug_dict['bug_user_done'] = bug.bug_user_done
        bug_dict['bug_version'] = bug.bug_version
        user = get_user_by_id(self, bug.bug_user_done)
        if user is not None:
            bug_dict['bug_user_done'] = user.username
        user_comp_belong = get_user_by_id(self, bug.component_belong)
        if user_comp_belong is not None:
            bug_dict['component_belong'] = user_comp_belong.username
        user_find_by = get_user_by_id(self, bug.bug_find_by)
        if user_find_by is not None:
            bug_dict['bug_find_by'] = user_find_by.username
        project_name = get_project_by_id(self, bug.bug_project_id)
        if project_name is not None:
            bug_dict['bug_project_id'] = project_name.project_name
        comp_name = get_project_by_id(self, bug.bug_component)
        if comp_name is not None:
            bug_dict['bug_component'] = comp_name.project_name
        result.append(bug_dict)
    return result


class BugTrackHandler(BaseHandler):
    @authenticated
    def get(self):
        belongid = self.get_argument("belongid", None)
        compid = self.get_argument("compid", None)
        blevel = self.get_argument("blevel", None)
        weblog.info("%s.", self._request_summary())
        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid, blevel),
                           users=get_user_list(self), projects=get_project_list(self))
        # return self.render('bug/bugtracklist.html', message="", users=get_user_list(self)
        #                    , projects=get_project_list(self), bugs=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_component = int(self.get_argument("bug_component", '-1'))
        component_belong = int(self.get_argument("component_belong", '-1'))
        bug_level = int(self.get_argument("bug_level", '-1'))
        bug_component = None if bug_component < 0 else bug_component
        component_belong = None if component_belong < 0 else component_belong
        bug_level = None if bug_level < 0 else bug_level
        bugtracks = get_bugtrack_list(self, component_belong, bug_component, bug_level)
        weblog.info("%s. %d %d %d", self._request_summary(), bug_component, component_belong, bug_level)

        return self.write(json.dumps(bugtracks))


class BugTrackAddHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtrackadd.html')
        return self.render('bug/bugtrackadd.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track = TblBugTrack()
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().add(bug_track)
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackEditHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid))
        return self.render('bug/bugtrackedit.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self), bug=get_bugtrack_by_id(self, bid))

    @authenticated
    def post(self, bid):
        weblog.info("%s.", self._request_summary())
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bid).first()
        if bug_track is None:
            msg.append(u"获取问题单为空，问题单id={}".format(bid))
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackedit.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackDeleteHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        bug_track = self.mysqldb().query(TblBugTrack).filter_by(comp_id=bid).first()
        bug_track.bug_project_id = -1
        try:
            self.mysqldb().commit()
        except Exception as e:
            weblog.error("delete bug track id={} error. {}".format(bid, e))
            self.mysqldb().rollback()

        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        # coding=utf-8
import json
from database.tbl_project import TblProject
from database.tbl_bug_list import TblBugList
from database.tbl_account import TblAccount
from database.tbl_bug_track import TblBugTrack
from database.tbl_project_user import TblPorjectUser
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
from tornado.log import access_log as weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord
from handlers.user_manage_handler import get_user_list, get_user_by_id
from handlers.Project.project_manage_handler import get_project_list, get_project_by_id


def get_bugtrack_list(self, belongid=None, compid=None, level=None):
    bugs = self.mysqldb().query(TblBugTrack)
    if belongid is not None:
        bugs = bugs.filter(TblBugTrack.component_belong == belongid)
    if compid is not None:
        bugs = bugs.filter(TblBugTrack.bug_component == compid)
    if level is not None:
        bugs = bugs.filter(TblBugTrack.bug_level == level)
    bugs = bugs.filter(TblBugTrack.bug_project_id > 0)
    bugs = bugs.order_by(TblBugTrack.bug_date_receive.desc())
    bugs = bugs.all()
    # for project in projects:
    #     print(project.describe,type(project.describe))
    result = gene_bugtrack_result(self, bugs)
    return result


def get_bugtrack_by_id(self, bug_id):
    bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bug_id).first()
    result = gene_bugtrack_result(self, [bug_track])
    if result:
        return result[0]
    else:
        return []


def gene_bugtrack_result(self, bugs):
    result = []
    for bug in bugs:
        bug_dict = dict()
        bug_dict['bug_id'] = bug.bug_id
        bug_dict['bug_date_receive'] = str(bug.bug_date_receive)
        bug_dict['bug_find_by'] = bug.bug_find_by
        bug_dict['bug_component'] = bug.bug_component
        bug_dict['component_belong'] = bug.component_belong
        bug_dict['component_community'] = bug.component_community
        bug_dict['bug_project_id'] = bug.bug_project_id
        bug_dict['project_version'] = bug.project_version
        bug_dict['bug_describe'] = bug.bug_describe
        bug_dict['bug_level'] = msg_define.BUG_LEVEL[bug.bug_level]
        bug_dict['bug_reason'] = bug.bug_reason
        bug_dict['bug_solution'] = bug.bug_solution
        bug_dict['bug_progress'] = bug.bug_progress
        bug_dict['bug_date_plan'] = str(bug.bug_date_plan)
        bug_dict['bug_date_done'] = str(bug.bug_date_done)
        bug_dict['bug_user_done'] = bug.bug_user_done
        bug_dict['bug_version'] = bug.bug_version
        user = get_user_by_id(self, bug.bug_user_done)
        if user is not None:
            bug_dict['bug_user_done'] = user.username
        user_comp_belong = get_user_by_id(self, bug.component_belong)
        if user_comp_belong is not None:
            bug_dict['component_belong'] = user_comp_belong.username
        user_find_by = get_user_by_id(self, bug.bug_find_by)
        if user_find_by is not None:
            bug_dict['bug_find_by'] = user_find_by.username
        project_name = get_project_by_id(self, bug.bug_project_id)
        if project_name is not None:
            bug_dict['bug_project_id'] = project_name.project_name
        comp_name = get_project_by_id(self, bug.bug_component)
        if comp_name is not None:
            bug_dict['bug_component'] = comp_name.project_name
        result.append(bug_dict)
    return result


class BugTrackHandler(BaseHandler):
    @authenticated
    def get(self):
        belongid = self.get_argument("belongid", None)
        compid = self.get_argument("compid", None)
        blevel = self.get_argument("blevel", None)
        weblog.info("%s.", self._request_summary())
        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid, blevel),
                           users=get_user_list(self), projects=get_project_list(self))
        # return self.render('bug/bugtracklist.html', message="", users=get_user_list(self)
        #                    , projects=get_project_list(self), bugs=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_component = int(self.get_argument("bug_component", '-1'))
        component_belong = int(self.get_argument("component_belong", '-1'))
        bug_level = int(self.get_argument("bug_level", '-1'))
        bug_component = None if bug_component < 0 else bug_component
        component_belong = None if component_belong < 0 else component_belong
        bug_level = None if bug_level < 0 else bug_level
        bugtracks = get_bugtrack_list(self, component_belong, bug_component, bug_level)
        weblog.info("%s. %d %d %d", self._request_summary(), bug_component, component_belong, bug_level)

        return self.write(json.dumps(bugtracks))


class BugTrackAddHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtrackadd.html')
        return self.render('bug/bugtrackadd.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track = TblBugTrack()
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().add(bug_track)
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackEditHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid))
        return self.render('bug/bugtrackedit.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self), bug=get_bugtrack_by_id(self, bid))

    @authenticated
    def post(self, bid):
        weblog.info("%s.", self._request_summary())
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bid).first()
        if bug_track is None:
            msg.append(u"获取问题单为空，问题单id={}".format(bid))
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackedit.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackDeleteHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        bug_track = self.mysqldb().query(TblBugTrack).filter_by(comp_id=bid).first()
        bug_track.bug_project_id = -1
        try:
            self.mysqldb().commit()
        except Exception as e:
            weblog.error("delete bug track id={} error. {}".format(bid, e))
            self.mysqldb().rollback()

        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        # coding=utf-8
import json
from database.tbl_project import TblProject
from database.tbl_bug_list import TblBugList
from database.tbl_account import TblAccount
from database.tbl_bug_track import TblBugTrack
from database.tbl_project_user import TblPorjectUser
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
from tornado.log import access_log as weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord
from handlers.user_manage_handler import get_user_list, get_user_by_id
from handlers.Project.project_manage_handler import get_project_list, get_project_by_id


def get_bugtrack_list(self, belongid=None, compid=None, level=None):
    bugs = self.mysqldb().query(TblBugTrack)
    if belongid is not None:
        bugs = bugs.filter(TblBugTrack.component_belong == belongid)
    if compid is not None:
        bugs = bugs.filter(TblBugTrack.bug_component == compid)
    if level is not None:
        bugs = bugs.filter(TblBugTrack.bug_level == level)
    bugs = bugs.filter(TblBugTrack.bug_project_id > 0)
    bugs = bugs.order_by(TblBugTrack.bug_date_receive.desc())
    bugs = bugs.all()
    # for project in projects:
    #     print(project.describe,type(project.describe))
    result = gene_bugtrack_result(self, bugs)
    return result


def get_bugtrack_by_id(self, bug_id):
    bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bug_id).first()
    result = gene_bugtrack_result(self, [bug_track])
    if result:
        return result[0]
    else:
        return []


def gene_bugtrack_result(self, bugs):
    result = []
    for bug in bugs:
        bug_dict = dict()
        bug_dict['bug_id'] = bug.bug_id
        bug_dict['bug_date_receive'] = str(bug.bug_date_receive)
        bug_dict['bug_find_by'] = bug.bug_find_by
        bug_dict['bug_component'] = bug.bug_component
        bug_dict['component_belong'] = bug.component_belong
        bug_dict['component_community'] = bug.component_community
        bug_dict['bug_project_id'] = bug.bug_project_id
        bug_dict['project_version'] = bug.project_version
        bug_dict['bug_describe'] = bug.bug_describe
        bug_dict['bug_level'] = msg_define.BUG_LEVEL[bug.bug_level]
        bug_dict['bug_reason'] = bug.bug_reason
        bug_dict['bug_solution'] = bug.bug_solution
        bug_dict['bug_progress'] = bug.bug_progress
        bug_dict['bug_date_plan'] = str(bug.bug_date_plan)
        bug_dict['bug_date_done'] = str(bug.bug_date_done)
        bug_dict['bug_user_done'] = bug.bug_user_done
        bug_dict['bug_version'] = bug.bug_version
        user = get_user_by_id(self, bug.bug_user_done)
        if user is not None:
            bug_dict['bug_user_done'] = user.username
        user_comp_belong = get_user_by_id(self, bug.component_belong)
        if user_comp_belong is not None:
            bug_dict['component_belong'] = user_comp_belong.username
        user_find_by = get_user_by_id(self, bug.bug_find_by)
        if user_find_by is not None:
            bug_dict['bug_find_by'] = user_find_by.username
        project_name = get_project_by_id(self, bug.bug_project_id)
        if project_name is not None:
            bug_dict['bug_project_id'] = project_name.project_name
        comp_name = get_project_by_id(self, bug.bug_component)
        if comp_name is not None:
            bug_dict['bug_component'] = comp_name.project_name
        result.append(bug_dict)
    return result


class BugTrackHandler(BaseHandler):
    @authenticated
    def get(self):
        belongid = self.get_argument("belongid", None)
        compid = self.get_argument("compid", None)
        blevel = self.get_argument("blevel", None)
        weblog.info("%s.", self._request_summary())
        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid, blevel),
                           users=get_user_list(self), projects=get_project_list(self))
        # return self.render('bug/bugtracklist.html', message="", users=get_user_list(self)
        #                    , projects=get_project_list(self), bugs=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_component = int(self.get_argument("bug_component", '-1'))
        component_belong = int(self.get_argument("component_belong", '-1'))
        bug_level = int(self.get_argument("bug_level", '-1'))
        bug_component = None if bug_component < 0 else bug_component
        component_belong = None if component_belong < 0 else component_belong
        bug_level = None if bug_level < 0 else bug_level
        bugtracks = get_bugtrack_list(self, component_belong, bug_component, bug_level)
        weblog.info("%s. %d %d %d", self._request_summary(), bug_component, component_belong, bug_level)

        return self.write(json.dumps(bugtracks))


class BugTrackAddHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtrackadd.html')
        return self.render('bug/bugtrackadd.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track = TblBugTrack()
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().add(bug_track)
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackEditHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid))
        return self.render('bug/bugtrackedit.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self), bug=get_bugtrack_by_id(self, bid))

    @authenticated
    def post(self, bid):
        weblog.info("%s.", self._request_summary())
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bid).first()
        if bug_track is None:
            msg.append(u"获取问题单为空，问题单id={}".format(bid))
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackedit.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackDeleteHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        bug_track = self.mysqldb().query(TblBugTrack).filter_by(comp_id=bid).first()
        bug_track.bug_project_id = -1
        try:
            self.mysqldb().commit()
        except Exception as e:
            weblog.error("delete bug track id={} error. {}".format(bid, e))
            self.mysqldb().rollback()

        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        # coding=utf-8
import json
from database.tbl_project import TblProject
from database.tbl_bug_list import TblBugList
from database.tbl_account import TblAccount
from database.tbl_bug_track import TblBugTrack
from database.tbl_project_user import TblPorjectUser
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
from tornado.log import access_log as weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord
from handlers.user_manage_handler import get_user_list, get_user_by_id
from handlers.Project.project_manage_handler import get_project_list, get_project_by_id


def get_bugtrack_list(self, belongid=None, compid=None, level=None):
    bugs = self.mysqldb().query(TblBugTrack)
    if belongid is not None:
        bugs = bugs.filter(TblBugTrack.component_belong == belongid)
    if compid is not None:
        bugs = bugs.filter(TblBugTrack.bug_component == compid)
    if level is not None:
        bugs = bugs.filter(TblBugTrack.bug_level == level)
    bugs = bugs.filter(TblBugTrack.bug_project_id > 0)
    bugs = bugs.order_by(TblBugTrack.bug_date_receive.desc())
    bugs = bugs.all()
    # for project in projects:
    #     print(project.describe,type(project.describe))
    result = gene_bugtrack_result(self, bugs)
    return result


def get_bugtrack_by_id(self, bug_id):
    bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bug_id).first()
    result = gene_bugtrack_result(self, [bug_track])
    if result:
        return result[0]
    else:
        return []


def gene_bugtrack_result(self, bugs):
    result = []
    for bug in bugs:
        bug_dict = dict()
        bug_dict['bug_id'] = bug.bug_id
        bug_dict['bug_date_receive'] = str(bug.bug_date_receive)
        bug_dict['bug_find_by'] = bug.bug_find_by
        bug_dict['bug_component'] = bug.bug_component
        bug_dict['component_belong'] = bug.component_belong
        bug_dict['component_community'] = bug.component_community
        bug_dict['bug_project_id'] = bug.bug_project_id
        bug_dict['project_version'] = bug.project_version
        bug_dict['bug_describe'] = bug.bug_describe
        bug_dict['bug_level'] = msg_define.BUG_LEVEL[bug.bug_level]
        bug_dict['bug_reason'] = bug.bug_reason
        bug_dict['bug_solution'] = bug.bug_solution
        bug_dict['bug_progress'] = bug.bug_progress
        bug_dict['bug_date_plan'] = str(bug.bug_date_plan)
        bug_dict['bug_date_done'] = str(bug.bug_date_done)
        bug_dict['bug_user_done'] = bug.bug_user_done
        bug_dict['bug_version'] = bug.bug_version
        user = get_user_by_id(self, bug.bug_user_done)
        if user is not None:
            bug_dict['bug_user_done'] = user.username
        user_comp_belong = get_user_by_id(self, bug.component_belong)
        if user_comp_belong is not None:
            bug_dict['component_belong'] = user_comp_belong.username
        user_find_by = get_user_by_id(self, bug.bug_find_by)
        if user_find_by is not None:
            bug_dict['bug_find_by'] = user_find_by.username
        project_name = get_project_by_id(self, bug.bug_project_id)
        if project_name is not None:
            bug_dict['bug_project_id'] = project_name.project_name
        comp_name = get_project_by_id(self, bug.bug_component)
        if comp_name is not None:
            bug_dict['bug_component'] = comp_name.project_name
        result.append(bug_dict)
    return result


class BugTrackHandler(BaseHandler):
    @authenticated
    def get(self):
        belongid = self.get_argument("belongid", None)
        compid = self.get_argument("compid", None)
        blevel = self.get_argument("blevel", None)
        weblog.info("%s.", self._request_summary())
        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid, blevel),
                           users=get_user_list(self), projects=get_project_list(self))
        # return self.render('bug/bugtracklist.html', message="", users=get_user_list(self)
        #                    , projects=get_project_list(self), bugs=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_component = int(self.get_argument("bug_component", '-1'))
        component_belong = int(self.get_argument("component_belong", '-1'))
        bug_level = int(self.get_argument("bug_level", '-1'))
        bug_component = None if bug_component < 0 else bug_component
        component_belong = None if component_belong < 0 else component_belong
        bug_level = None if bug_level < 0 else bug_level
        bugtracks = get_bugtrack_list(self, component_belong, bug_component, bug_level)
        weblog.info("%s. %d %d %d", self._request_summary(), bug_component, component_belong, bug_level)

        return self.write(json.dumps(bugtracks))


class BugTrackAddHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtrackadd.html')
        return self.render('bug/bugtrackadd.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track = TblBugTrack()
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().add(bug_track)
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackEditHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid))
        return self.render('bug/bugtrackedit.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self), bug=get_bugtrack_by_id(self, bid))

    @authenticated
    def post(self, bid):
        weblog.info("%s.", self._request_summary())
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bid).first()
        if bug_track is None:
            msg.append(u"获取问题单为空，问题单id={}".format(bid))
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackedit.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackDeleteHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        bug_track = self.mysqldb().query(TblBugTrack).filter_by(comp_id=bid).first()
        bug_track.bug_project_id = -1
        try:
            self.mysqldb().commit()
        except Exception as e:
            weblog.error("delete bug track id={} error. {}".format(bid, e))
            self.mysqldb().rollback()

        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        # coding=utf-8
import json
from database.tbl_project import TblProject
from database.tbl_bug_list import TblBugList
from database.tbl_account import TblAccount
from database.tbl_bug_track import TblBugTrack
from database.tbl_project_user import TblPorjectUser
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
from tornado.log import access_log as weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord
from handlers.user_manage_handler import get_user_list, get_user_by_id
from handlers.Project.project_manage_handler import get_project_list, get_project_by_id


def get_bugtrack_list(self, belongid=None, compid=None, level=None):
    bugs = self.mysqldb().query(TblBugTrack)
    if belongid is not None:
        bugs = bugs.filter(TblBugTrack.component_belong == belongid)
    if compid is not None:
        bugs = bugs.filter(TblBugTrack.bug_component == compid)
    if level is not None:
        bugs = bugs.filter(TblBugTrack.bug_level == level)
    bugs = bugs.filter(TblBugTrack.bug_project_id > 0)
    bugs = bugs.order_by(TblBugTrack.bug_date_receive.desc())
    bugs = bugs.all()
    # for project in projects:
    #     print(project.describe,type(project.describe))
    result = gene_bugtrack_result(self, bugs)
    return result


def get_bugtrack_by_id(self, bug_id):
    bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bug_id).first()
    result = gene_bugtrack_result(self, [bug_track])
    if result:
        return result[0]
    else:
        return []


def gene_bugtrack_result(self, bugs):
    result = []
    for bug in bugs:
        bug_dict = dict()
        bug_dict['bug_id'] = bug.bug_id
        bug_dict['bug_date_receive'] = str(bug.bug_date_receive)
        bug_dict['bug_find_by'] = bug.bug_find_by
        bug_dict['bug_component'] = bug.bug_component
        bug_dict['component_belong'] = bug.component_belong
        bug_dict['component_community'] = bug.component_community
        bug_dict['bug_project_id'] = bug.bug_project_id
        bug_dict['project_version'] = bug.project_version
        bug_dict['bug_describe'] = bug.bug_describe
        bug_dict['bug_level'] = msg_define.BUG_LEVEL[bug.bug_level]
        bug_dict['bug_reason'] = bug.bug_reason
        bug_dict['bug_solution'] = bug.bug_solution
        bug_dict['bug_progress'] = bug.bug_progress
        bug_dict['bug_date_plan'] = str(bug.bug_date_plan)
        bug_dict['bug_date_done'] = str(bug.bug_date_done)
        bug_dict['bug_user_done'] = bug.bug_user_done
        bug_dict['bug_version'] = bug.bug_version
        user = get_user_by_id(self, bug.bug_user_done)
        if user is not None:
            bug_dict['bug_user_done'] = user.username
        user_comp_belong = get_user_by_id(self, bug.component_belong)
        if user_comp_belong is not None:
            bug_dict['component_belong'] = user_comp_belong.username
        user_find_by = get_user_by_id(self, bug.bug_find_by)
        if user_find_by is not None:
            bug_dict['bug_find_by'] = user_find_by.username
        project_name = get_project_by_id(self, bug.bug_project_id)
        if project_name is not None:
            bug_dict['bug_project_id'] = project_name.project_name
        comp_name = get_project_by_id(self, bug.bug_component)
        if comp_name is not None:
            bug_dict['bug_component'] = comp_name.project_name
        result.append(bug_dict)
    return result


class BugTrackHandler(BaseHandler):
    @authenticated
    def get(self):
        belongid = self.get_argument("belongid", None)
        compid = self.get_argument("compid", None)
        blevel = self.get_argument("blevel", None)
        weblog.info("%s.", self._request_summary())
        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid, blevel),
                           users=get_user_list(self), projects=get_project_list(self))
        # return self.render('bug/bugtracklist.html', message="", users=get_user_list(self)
        #                    , projects=get_project_list(self), bugs=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_component = int(self.get_argument("bug_component", '-1'))
        component_belong = int(self.get_argument("component_belong", '-1'))
        bug_level = int(self.get_argument("bug_level", '-1'))
        bug_component = None if bug_component < 0 else bug_component
        component_belong = None if component_belong < 0 else component_belong
        bug_level = None if bug_level < 0 else bug_level
        bugtracks = get_bugtrack_list(self, component_belong, bug_component, bug_level)
        weblog.info("%s. %d %d %d", self._request_summary(), bug_component, component_belong, bug_level)

        return self.write(json.dumps(bugtracks))


class BugTrackAddHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtrackadd.html')
        return self.render('bug/bugtrackadd.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track = TblBugTrack()
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().add(bug_track)
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackEditHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid))
        return self.render('bug/bugtrackedit.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self), bug=get_bugtrack_by_id(self, bid))

    @authenticated
    def post(self, bid):
        weblog.info("%s.", self._request_summary())
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bid).first()
        if bug_track is None:
            msg.append(u"获取问题单为空，问题单id={}".format(bid))
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackedit.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackDeleteHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        bug_track = self.mysqldb().query(TblBugTrack).filter_by(comp_id=bid).first()
        bug_track.bug_project_id = -1
        try:
            self.mysqldb().commit()
        except Exception as e:
            weblog.error("delete bug track id={} error. {}".format(bid, e))
            self.mysqldb().rollback()

        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        # coding=utf-8
import json
from database.tbl_project import TblProject
from database.tbl_bug_list import TblBugList
from database.tbl_account import TblAccount
from database.tbl_bug_track import TblBugTrack
from database.tbl_project_user import TblPorjectUser
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
from tornado.log import access_log as weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord
from handlers.user_manage_handler import get_user_list, get_user_by_id
from handlers.Project.project_manage_handler import get_project_list, get_project_by_id


def get_bugtrack_list(self, belongid=None, compid=None, level=None):
    bugs = self.mysqldb().query(TblBugTrack)
    if belongid is not None:
        bugs = bugs.filter(TblBugTrack.component_belong == belongid)
    if compid is not None:
        bugs = bugs.filter(TblBugTrack.bug_component == compid)
    if level is not None:
        bugs = bugs.filter(TblBugTrack.bug_level == level)
    bugs = bugs.filter(TblBugTrack.bug_project_id > 0)
    bugs = bugs.order_by(TblBugTrack.bug_date_receive.desc())
    bugs = bugs.all()
    # for project in projects:
    #     print(project.describe,type(project.describe))
    result = gene_bugtrack_result(self, bugs)
    return result


def get_bugtrack_by_id(self, bug_id):
    bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bug_id).first()
    result = gene_bugtrack_result(self, [bug_track])
    if result:
        return result[0]
    else:
        return []


def gene_bugtrack_result(self, bugs):
    result = []
    for bug in bugs:
        bug_dict = dict()
        bug_dict['bug_id'] = bug.bug_id
        bug_dict['bug_date_receive'] = str(bug.bug_date_receive)
        bug_dict['bug_find_by'] = bug.bug_find_by
        bug_dict['bug_component'] = bug.bug_component
        bug_dict['component_belong'] = bug.component_belong
        bug_dict['component_community'] = bug.component_community
        bug_dict['bug_project_id'] = bug.bug_project_id
        bug_dict['project_version'] = bug.project_version
        bug_dict['bug_describe'] = bug.bug_describe
        bug_dict['bug_level'] = msg_define.BUG_LEVEL[bug.bug_level]
        bug_dict['bug_reason'] = bug.bug_reason
        bug_dict['bug_solution'] = bug.bug_solution
        bug_dict['bug_progress'] = bug.bug_progress
        bug_dict['bug_date_plan'] = str(bug.bug_date_plan)
        bug_dict['bug_date_done'] = str(bug.bug_date_done)
        bug_dict['bug_user_done'] = bug.bug_user_done
        bug_dict['bug_version'] = bug.bug_version
        user = get_user_by_id(self, bug.bug_user_done)
        if user is not None:
            bug_dict['bug_user_done'] = user.username
        user_comp_belong = get_user_by_id(self, bug.component_belong)
        if user_comp_belong is not None:
            bug_dict['component_belong'] = user_comp_belong.username
        user_find_by = get_user_by_id(self, bug.bug_find_by)
        if user_find_by is not None:
            bug_dict['bug_find_by'] = user_find_by.username
        project_name = get_project_by_id(self, bug.bug_project_id)
        if project_name is not None:
            bug_dict['bug_project_id'] = project_name.project_name
        comp_name = get_project_by_id(self, bug.bug_component)
        if comp_name is not None:
            bug_dict['bug_component'] = comp_name.project_name
        result.append(bug_dict)
    return result


class BugTrackHandler(BaseHandler):
    @authenticated
    def get(self):
        belongid = self.get_argument("belongid", None)
        compid = self.get_argument("compid", None)
        blevel = self.get_argument("blevel", None)
        weblog.info("%s.", self._request_summary())
        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid, blevel),
                           users=get_user_list(self), projects=get_project_list(self))
        # return self.render('bug/bugtracklist.html', message="", users=get_user_list(self)
        #                    , projects=get_project_list(self), bugs=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_component = int(self.get_argument("bug_component", '-1'))
        component_belong = int(self.get_argument("component_belong", '-1'))
        bug_level = int(self.get_argument("bug_level", '-1'))
        bug_component = None if bug_component < 0 else bug_component
        component_belong = None if component_belong < 0 else component_belong
        bug_level = None if bug_level < 0 else bug_level
        bugtracks = get_bugtrack_list(self, component_belong, bug_component, bug_level)
        weblog.info("%s. %d %d %d", self._request_summary(), bug_component, component_belong, bug_level)

        return self.write(json.dumps(bugtracks))


class BugTrackAddHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtrackadd.html')
        return self.render('bug/bugtrackadd.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track = TblBugTrack()
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().add(bug_track)
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackEditHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid))
        return self.render('bug/bugtrackedit.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self), bug=get_bugtrack_by_id(self, bid))

    @authenticated
    def post(self, bid):
        weblog.info("%s.", self._request_summary())
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bid).first()
        if bug_track is None:
            msg.append(u"获取问题单为空，问题单id={}".format(bid))
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackedit.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackDeleteHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        bug_track = self.mysqldb().query(TblBugTrack).filter_by(comp_id=bid).first()
        bug_track.bug_project_id = -1
        try:
            self.mysqldb().commit()
        except Exception as e:
            weblog.error("delete bug track id={} error. {}".format(bid, e))
            self.mysqldb().rollback()

        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        # coding=utf-8
import json
from database.tbl_project import TblProject
from database.tbl_bug_list import TblBugList
from database.tbl_account import TblAccount
from database.tbl_bug_track import TblBugTrack
from database.tbl_project_user import TblPorjectUser
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
from tornado.log import access_log as weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord
from handlers.user_manage_handler import get_user_list, get_user_by_id
from handlers.Project.project_manage_handler import get_project_list, get_project_by_id


def get_bugtrack_list(self, belongid=None, compid=None, level=None):
    bugs = self.mysqldb().query(TblBugTrack)
    if belongid is not None:
        bugs = bugs.filter(TblBugTrack.component_belong == belongid)
    if compid is not None:
        bugs = bugs.filter(TblBugTrack.bug_component == compid)
    if level is not None:
        bugs = bugs.filter(TblBugTrack.bug_level == level)
    bugs = bugs.filter(TblBugTrack.bug_project_id > 0)
    bugs = bugs.order_by(TblBugTrack.bug_date_receive.desc())
    bugs = bugs.all()
    # for project in projects:
    #     print(project.describe,type(project.describe))
    result = gene_bugtrack_result(self, bugs)
    return result


def get_bugtrack_by_id(self, bug_id):
    bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bug_id).first()
    result = gene_bugtrack_result(self, [bug_track])
    if result:
        return result[0]
    else:
        return []


def gene_bugtrack_result(self, bugs):
    result = []
    for bug in bugs:
        bug_dict = dict()
        bug_dict['bug_id'] = bug.bug_id
        bug_dict['bug_date_receive'] = str(bug.bug_date_receive)
        bug_dict['bug_find_by'] = bug.bug_find_by
        bug_dict['bug_component'] = bug.bug_component
        bug_dict['component_belong'] = bug.component_belong
        bug_dict['component_community'] = bug.component_community
        bug_dict['bug_project_id'] = bug.bug_project_id
        bug_dict['project_version'] = bug.project_version
        bug_dict['bug_describe'] = bug.bug_describe
        bug_dict['bug_level'] = msg_define.BUG_LEVEL[bug.bug_level]
        bug_dict['bug_reason'] = bug.bug_reason
        bug_dict['bug_solution'] = bug.bug_solution
        bug_dict['bug_progress'] = bug.bug_progress
        bug_dict['bug_date_plan'] = str(bug.bug_date_plan)
        bug_dict['bug_date_done'] = str(bug.bug_date_done)
        bug_dict['bug_user_done'] = bug.bug_user_done
        bug_dict['bug_version'] = bug.bug_version
        user = get_user_by_id(self, bug.bug_user_done)
        if user is not None:
            bug_dict['bug_user_done'] = user.username
        user_comp_belong = get_user_by_id(self, bug.component_belong)
        if user_comp_belong is not None:
            bug_dict['component_belong'] = user_comp_belong.username
        user_find_by = get_user_by_id(self, bug.bug_find_by)
        if user_find_by is not None:
            bug_dict['bug_find_by'] = user_find_by.username
        project_name = get_project_by_id(self, bug.bug_project_id)
        if project_name is not None:
            bug_dict['bug_project_id'] = project_name.project_name
        comp_name = get_project_by_id(self, bug.bug_component)
        if comp_name is not None:
            bug_dict['bug_component'] = comp_name.project_name
        result.append(bug_dict)
    return result


class BugTrackHandler(BaseHandler):
    @authenticated
    def get(self):
        belongid = self.get_argument("belongid", None)
        compid = self.get_argument("compid", None)
        blevel = self.get_argument("blevel", None)
        weblog.info("%s.", self._request_summary())
        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid, blevel),
                           users=get_user_list(self), projects=get_project_list(self))
        # return self.render('bug/bugtracklist.html', message="", users=get_user_list(self)
        #                    , projects=get_project_list(self), bugs=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_component = int(self.get_argument("bug_component", '-1'))
        component_belong = int(self.get_argument("component_belong", '-1'))
        bug_level = int(self.get_argument("bug_level", '-1'))
        bug_component = None if bug_component < 0 else bug_component
        component_belong = None if component_belong < 0 else component_belong
        bug_level = None if bug_level < 0 else bug_level
        bugtracks = get_bugtrack_list(self, component_belong, bug_component, bug_level)
        weblog.info("%s. %d %d %d", self._request_summary(), bug_component, component_belong, bug_level)

        return self.write(json.dumps(bugtracks))


class BugTrackAddHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtrackadd.html')
        return self.render('bug/bugtrackadd.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track = TblBugTrack()
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().add(bug_track)
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackEditHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid))
        return self.render('bug/bugtrackedit.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self), bug=get_bugtrack_by_id(self, bid))

    @authenticated
    def post(self, bid):
        weblog.info("%s.", self._request_summary())
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bid).first()
        if bug_track is None:
            msg.append(u"获取问题单为空，问题单id={}".format(bid))
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackedit.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackDeleteHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        bug_track = self.mysqldb().query(TblBugTrack).filter_by(comp_id=bid).first()
        bug_track.bug_project_id = -1
        try:
            self.mysqldb().commit()
        except Exception as e:
            weblog.error("delete bug track id={} error. {}".format(bid, e))
            self.mysqldb().rollback()

        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
"""
import json

# from database.tbl_project import TblProject
# from database.tbl_bug_list import TblBugList
# from database.tbl_account import TblAccount
# from database.tbl_bug_track import TblBugTrack
# from database.tbl_project_user import TblPorjectUser
# from handlers.base_handler import BaseHandler
# from tornado.web import authenticated
# from tornado.log import access_log as weblog
# from message import msg_define
# from handlers.Email.email_smtp_handler import check_email, check_passord
# from handlers.user_manage_handler import get_user_list, get_user_by_id
# from handlers.Project.project_manage_handler import get_project_list, get_project_by_id
#
#
# def get_bugtrack_list(self, belongid=None, compid=None, level=None):
#     bugs = self.mysqldb().query(TblBugTrack)
#     if belongid is not None:
#         bugs = bugs.filter(TblBugTrack.component_belong == belongid)
#     if compid is not None:
#         bugs = bugs.filter(TblBugTrack.bug_component == compid)
#     if level is not None:
#         bugs = bugs.filter(TblBugTrack.bug_level == level)
#     bugs = bugs.filter(TblBugTrack.bug_project_id > 0)
#     bugs = bugs.order_by(TblBugTrack.bug_date_receive.desc())
#     bugs = bugs.all()
#     # for project in projects:
#     #     print(project.describe,type(project.describe))
#     result = gene_bugtrack_result(self, bugs)
#     return result
#
#
# def get_bugtrack_by_id(self, bug_id):
#     bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bug_id).first()
#     result = gene_bugtrack_result(self, [bug_track])
#     if result:
#         return result[0]
#     else:
#         return []
#
#
# def gene_bugtrack_result(self, bugs):
#     result = []
#     for bug in bugs:
#         bug_dict = dict()
#         bug_dict['bug_id'] = bug.bug_id
#         bug_dict['bug_date_receive'] = str(bug.bug_date_receive)
#         bug_dict['bug_find_by'] = bug.bug_find_by
#         bug_dict['bug_component'] = bug.bug_component
#         bug_dict['component_belong'] = bug.component_belong
#         bug_dict['component_community'] = bug.component_community
#         bug_dict['bug_project_id'] = bug.bug_project_id
#         bug_dict['project_version'] = bug.project_version
#         bug_dict['bug_describe'] = bug.bug_describe
#         bug_dict['bug_level'] = msg_define.BUG_LEVEL[bug.bug_level]
#         bug_dict['bug_reason'] = bug.bug_reason
#         bug_dict['bug_solution'] = bug.bug_solution
#         bug_dict['bug_progress'] = bug.bug_progress
#         bug_dict['bug_date_plan'] = str(bug.bug_date_plan)
#         bug_dict['bug_date_done'] = str(bug.bug_date_done)
#         bug_dict['bug_user_done'] = bug.bug_user_done
#         bug_dict['bug_version'] = bug.bug_version
#         user = get_user_by_id(self, bug.bug_user_done)
#         if user is not None:
#             bug_dict['bug_user_done'] = user.username
#         user_comp_belong = get_user_by_id(self, bug.component_belong)
#         if user_comp_belong is not None:
#             bug_dict['component_belong'] = user_comp_belong.username
#         user_find_by = get_user_by_id(self, bug.bug_find_by)
#         if user_find_by is not None:
#             bug_dict['bug_find_by'] = user_find_by.username
#         project_name = get_project_by_id(self, bug.bug_project_id)
#         if project_name is not None:
#             bug_dict['bug_project_id'] = project_name.project_name
#         comp_name = get_project_by_id(self, bug.bug_component)
#         if comp_name is not None:
#             bug_dict['bug_component'] = comp_name.project_name
#         result.append(bug_dict)
#     return result
#
#
# class BugTrackHandler(BaseHandler):
#     @authenticated
#     def get(self):
#         belongid = self.get_argument("belongid", None)
#         compid = self.get_argument("compid", None)
#         blevel = self.get_argument("blevel", None)
#         weblog.info("%s.", self._request_summary())
#         return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid, blevel),
#                            users=get_user_list(self), projects=get_project_list(self))
#         # return self.render('bug/bugtracklist.html', message="", users=get_user_list(self)
#         #                    , projects=get_project_list(self), bugs=get_bugtrack_list(self))
#
#     @authenticated
#     def post(self):
#         weblog.info("%s.", self._request_summary())
#         bug_component = int(self.get_argument("bug_component", '-1'))
#         component_belong = int(self.get_argument("component_belong", '-1'))
#         bug_level = int(self.get_argument("bug_level", '-1'))
#         bug_component = None if bug_component < 0 else bug_component
#         component_belong = None if component_belong < 0 else component_belong
#         bug_level = None if bug_level < 0 else bug_level
#         bugtracks = get_bugtrack_list(self, component_belong, bug_component, bug_level)
#         weblog.info("%s. %d %d %d", self._request_summary(), bug_component, component_belong, bug_level)
#
#         return self.write(json.dumps(bugtracks))
#
#
# class BugTrackAddHandler(BaseHandler):
#     @authenticated
#     def get(self):
#         weblog.info("%s.", self._request_summary())
#         # return self.render('bug/bugtrackadd.html')
#         return self.render('bug/bugtrackadd.html', message="", users=get_user_list(self)
#                            , projects=get_project_list(self))
#
#     @authenticated
#     def post(self):
#         weblog.info("%s.", self._request_summary())
#         bug_date_receive = self.get_argument("bug_date_receive", None)
#         bug_find_by = int(self.get_argument("bug_find_by", 0))
#         bug_component = int(self.get_argument("bug_component", 0))
#         component_belong = int(self.get_argument("component_belong", 0))
#         component_community = self.get_argument("component_community", None)
#         bug_project_id = int(self.get_argument("bug_project_id", 0))
#         # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
#         project_version = self.get_argument("project_version", None)
#         bug_describe = self.get_argument("bug_describe", None)
#         bug_level = int(self.get_argument("bug_level", 0))
#         bug_reason = self.get_argument("bug_reason", None)
#         bug_solution = self.get_argument("bug_solution", None)
#         bug_progress = self.get_argument("bug_progress", None)
#         bug_date_plan = self.get_argument("bug_date_plan", None)
#         bug_date_done = self.get_argument("bug_date_done", None)
#         bug_user_done = int(self.get_argument("bug_user_done", 0))
#         bug_version = self.get_argument("bug_version", None)
#         msg = []
#         if bug_date_receive is None:
#             msg.append(u"接收日期不能为空")
#         if project_version is None:
#             msg.append(u"模块所属版本不能为空")
#         if bug_date_plan is None or bug_date_done is None:
#             msg.append(u"计划日期或解决日期不能为空")
#         if bug_version is None:
#             msg.append(u"合入版本不能为空")
#         if msg:
#             return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
#                                projects=get_project_list(self))
#         bug_track = TblBugTrack()
#         bug_track.bug_date_receive = bug_date_receive
#         bug_track.bug_find_by = bug_find_by
#         bug_track.bug_component = bug_component
#         bug_track.component_belong = component_belong
#         bug_track.component_community = component_community
#         bug_track.bug_project_id = bug_project_id
#         bug_track.project_version = project_version
#         bug_track.bug_describe = bug_describe
#         bug_track.bug_level = bug_level
#         bug_track.bug_reason = bug_reason
#         bug_track.bug_solution = bug_solution
#         bug_track.bug_progress = bug_progress
#         bug_track.bug_date_plan = bug_date_plan
#         bug_track.bug_date_done = bug_date_done
#         bug_track.bug_user_done = bug_user_done
#         bug_track.bug_version = bug_version
#
#         try:
#             self.mysqldb().add(bug_track)
#             self.mysqldb().commit()
#             return self.redirect("/bugtrack/list")
#         except Exception as e:
#             msg.append(e)
#             return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
#                                projects=get_project_list(self))
#
#
# class BugTrackEditHandler(BaseHandler):
#     @authenticated
#     def get(self, bid):
#         weblog.info("%s.", self._request_summary())
#         # return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid))
#         return self.render('bug/bugtrackedit.html', message="", users=get_user_list(self)
#                            , projects=get_project_list(self), bug=get_bugtrack_by_id(self, bid))
#
#     @authenticated
#     def post(self, bid):
#         weblog.info("%s.", self._request_summary())
#         weblog.info("%s.", self._request_summary())
#         bug_date_receive = self.get_argument("bug_date_receive", None)
#         bug_find_by = int(self.get_argument("bug_find_by", 0))
#         bug_component = int(self.get_argument("bug_component", 0))
#         component_belong = int(self.get_argument("component_belong", 0))
#         component_community = self.get_argument("component_community", None)
#         bug_project_id = int(self.get_argument("bug_project_id", 0))
#         # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
#         project_version = self.get_argument("project_version", None)
#         bug_describe = self.get_argument("bug_describe", None)
#         bug_level = int(self.get_argument("bug_level", 0))
#         bug_reason = self.get_argument("bug_reason", None)
#         bug_solution = self.get_argument("bug_solution", None)
#         bug_progress = self.get_argument("bug_progress", None)
#         bug_date_plan = self.get_argument("bug_date_plan", None)
#         bug_date_done = self.get_argument("bug_date_done", None)
#         bug_user_done = int(self.get_argument("bug_user_done", 0))
#         bug_version = self.get_argument("bug_version", None)
#         msg = []
#         if bug_date_receive is None:
#             msg.append(u"接收日期不能为空")
#         if project_version is None:
#             msg.append(u"模块所属版本不能为空")
#         if bug_date_plan is None or bug_date_done is None:
#             msg.append(u"计划日期或解决日期不能为空")
#         if bug_version is None:
#             msg.append(u"合入版本不能为空")
#         bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bid).first()
#         if bug_track is None:
#             msg.append(u"获取问题单为空，问题单id={}".format(bid))
#         if msg:
#             return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
#                                projects=get_project_list(self))
#         bug_track.bug_date_receive = bug_date_receive
#         bug_track.bug_find_by = bug_find_by
#         bug_track.bug_component = bug_component
#         bug_track.component_belong = component_belong
#         bug_track.component_community = component_community
#         bug_track.bug_project_id = bug_project_id
#         bug_track.project_version = project_version
#         bug_track.bug_describe = bug_describe
#         bug_track.bug_level = bug_level
#         bug_track.bug_reason = bug_reason
#         bug_track.bug_solution = bug_solution
#         bug_track.bug_progress = bug_progress
#         bug_track.bug_date_plan = bug_date_plan
#         bug_track.bug_date_done = bug_date_done
#         bug_track.bug_user_done = bug_user_done
#         bug_track.bug_version = bug_version
#
#         try:
#             self.mysqldb().commit()
#             return self.redirect("/bugtrack/list")
#         except Exception as e:
#             msg.append(e)
#             return self.render('bug/bugtrackedit.html', message=msg, users=get_user_list(self),
#                                projects=get_project_list(self))
#
#
# class BugTrackDeleteHandler(BaseHandler):
#     @authenticated
#     def get(self, bid):
#         weblog.info("%s.", self._request_summary())
#         bug_track = self.mysqldb().query(TblBugTrack).filter_by(comp_id=bid).first()
#         bug_track.bug_project_id = -1
#         try:
#             self.mysqldb().commit()
#         except Exception as e:
#             weblog.error("delete bug track id={} error. {}".format(bid, e))
#             self.mysqldb().rollback()
#
#         return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self))
#
#     @authenticated
#     def post(self):
#         weblog.info("%s.", self._request_summary())

"""
# coding=utf-8
import json
from database.tbl_project import TblProject
from database.tbl_bug_list import TblBugList
from database.tbl_account import TblAccount
from database.tbl_bug_track import TblBugTrack
from database.tbl_project_user import TblPorjectUser
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
from tornado.log import access_log as weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord
from handlers.user_manage_handler import get_user_list, get_user_by_id
from handlers.Project.project_manage_handler import get_project_list, get_project_by_id


def get_bugtrack_list(self, belongid=None, compid=None, level=None):
    bugs = self.mysqldb().query(TblBugTrack)
    if belongid is not None:
        bugs = bugs.filter(TblBugTrack.component_belong == belongid)
    if compid is not None:
        bugs = bugs.filter(TblBugTrack.bug_component == compid)
    if level is not None:
        bugs = bugs.filter(TblBugTrack.bug_level == level)
    bugs = bugs.filter(TblBugTrack.bug_project_id > 0)
    bugs = bugs.order_by(TblBugTrack.bug_date_receive.desc())
    bugs = bugs.all()
    # for project in projects:
    #     print(project.describe,type(project.describe))
    result = gene_bugtrack_result(self, bugs)
    return result


def get_bugtrack_by_id(self, bug_id):
    bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bug_id).first()
    result = gene_bugtrack_result(self, [bug_track])
    if result:
        return result[0]
    else:
        return []


def gene_bugtrack_result(self, bugs):
    result = []
    for bug in bugs:
        bug_dict = dict()
        bug_dict['bug_id'] = bug.bug_id
        bug_dict['bug_date_receive'] = str(bug.bug_date_receive)
        bug_dict['bug_find_by'] = bug.bug_find_by
        bug_dict['bug_component'] = bug.bug_component
        bug_dict['component_belong'] = bug.component_belong
        bug_dict['component_community'] = bug.component_community
        bug_dict['bug_project_id'] = bug.bug_project_id
        bug_dict['project_version'] = bug.project_version
        bug_dict['bug_describe'] = bug.bug_describe
        bug_dict['bug_level'] = msg_define.BUG_LEVEL[bug.bug_level]
        bug_dict['bug_reason'] = bug.bug_reason
        bug_dict['bug_solution'] = bug.bug_solution
        bug_dict['bug_progress'] = bug.bug_progress
        bug_dict['bug_date_plan'] = str(bug.bug_date_plan)
        bug_dict['bug_date_done'] = str(bug.bug_date_done)
        bug_dict['bug_user_done'] = bug.bug_user_done
        bug_dict['bug_version'] = bug.bug_version
        user = get_user_by_id(self, bug.bug_user_done)
        if user is not None:
            bug_dict['bug_user_done'] = user.username
        user_comp_belong = get_user_by_id(self, bug.component_belong)
        if user_comp_belong is not None:
            bug_dict['component_belong'] = user_comp_belong.username
        user_find_by = get_user_by_id(self, bug.bug_find_by)
        if user_find_by is not None:
            bug_dict['bug_find_by'] = user_find_by.username
        project_name = get_project_by_id(self, bug.bug_project_id)
        if project_name is not None:
            bug_dict['bug_project_id'] = project_name.project_name
        comp_name = get_project_by_id(self, bug.bug_component)
        if comp_name is not None:
            bug_dict['bug_component'] = comp_name.project_name
        result.append(bug_dict)
    return result


class BugTrackHandler(BaseHandler):
    @authenticated
    def get(self):
        belongid = self.get_argument("belongid", None)
        compid = self.get_argument("compid", None)
        blevel = self.get_argument("blevel", None)
        weblog.info("%s.", self._request_summary())
        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid, blevel),
                           users=get_user_list(self), projects=get_project_list(self))
        # return self.render('bug/bugtracklist.html', message="", users=get_user_list(self)
        #                    , projects=get_project_list(self), bugs=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_component = int(self.get_argument("bug_component", '-1'))
        component_belong = int(self.get_argument("component_belong", '-1'))
        bug_level = int(self.get_argument("bug_level", '-1'))
        bug_component = None if bug_component < 0 else bug_component
        component_belong = None if component_belong < 0 else component_belong
        bug_level = None if bug_level < 0 else bug_level
        bugtracks = get_bugtrack_list(self, component_belong, bug_component, bug_level)
        weblog.info("%s. %d %d %d", self._request_summary(), bug_component, component_belong, bug_level)

        return self.write(json.dumps(bugtracks))


class BugTrackAddHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtrackadd.html')
        return self.render('bug/bugtrackadd.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track = TblBugTrack()
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().add(bug_track)
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackEditHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid))
        return self.render('bug/bugtrackedit.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self), bug=get_bugtrack_by_id(self, bid))

    @authenticated
    def post(self, bid):
        weblog.info("%s.", self._request_summary())
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bid).first()
        if bug_track is None:
            msg.append(u"获取问题单为空，问题单id={}".format(bid))
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackedit.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackDeleteHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        bug_track = self.mysqldb().query(TblBugTrack).filter_by(comp_id=bid).first()
        bug_track.bug_project_id = -1
        try:
            self.mysqldb().commit()
        except Exception as e:
            weblog.error("delete bug track id={} error. {}".format(bid, e))
            self.mysqldb().rollback()

        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        # coding=utf-8
import json
from database.tbl_project import TblProject
from database.tbl_bug_list import TblBugList
from database.tbl_account import TblAccount
from database.tbl_bug_track import TblBugTrack
from database.tbl_project_user import TblPorjectUser
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
from tornado.log import access_log as weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord
from handlers.user_manage_handler import get_user_list, get_user_by_id
from handlers.Project.project_manage_handler import get_project_list, get_project_by_id


def get_bugtrack_list(self, belongid=None, compid=None, level=None):
    bugs = self.mysqldb().query(TblBugTrack)
    if belongid is not None:
        bugs = bugs.filter(TblBugTrack.component_belong == belongid)
    if compid is not None:
        bugs = bugs.filter(TblBugTrack.bug_component == compid)
    if level is not None:
        bugs = bugs.filter(TblBugTrack.bug_level == level)
    bugs = bugs.filter(TblBugTrack.bug_project_id > 0)
    bugs = bugs.order_by(TblBugTrack.bug_date_receive.desc())
    bugs = bugs.all()
    # for project in projects:
    #     print(project.describe,type(project.describe))
    result = gene_bugtrack_result(self, bugs)
    return result


def get_bugtrack_by_id(self, bug_id):
    bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bug_id).first()
    result = gene_bugtrack_result(self, [bug_track])
    if result:
        return result[0]
    else:
        return []


def gene_bugtrack_result(self, bugs):
    result = []
    for bug in bugs:
        bug_dict = dict()
        bug_dict['bug_id'] = bug.bug_id
        bug_dict['bug_date_receive'] = str(bug.bug_date_receive)
        bug_dict['bug_find_by'] = bug.bug_find_by
        bug_dict['bug_component'] = bug.bug_component
        bug_dict['component_belong'] = bug.component_belong
        bug_dict['component_community'] = bug.component_community
        bug_dict['bug_project_id'] = bug.bug_project_id
        bug_dict['project_version'] = bug.project_version
        bug_dict['bug_describe'] = bug.bug_describe
        bug_dict['bug_level'] = msg_define.BUG_LEVEL[bug.bug_level]
        bug_dict['bug_reason'] = bug.bug_reason
        bug_dict['bug_solution'] = bug.bug_solution
        bug_dict['bug_progress'] = bug.bug_progress
        bug_dict['bug_date_plan'] = str(bug.bug_date_plan)
        bug_dict['bug_date_done'] = str(bug.bug_date_done)
        bug_dict['bug_user_done'] = bug.bug_user_done
        bug_dict['bug_version'] = bug.bug_version
        user = get_user_by_id(self, bug.bug_user_done)
        if user is not None:
            bug_dict['bug_user_done'] = user.username
        user_comp_belong = get_user_by_id(self, bug.component_belong)
        if user_comp_belong is not None:
            bug_dict['component_belong'] = user_comp_belong.username
        user_find_by = get_user_by_id(self, bug.bug_find_by)
        if user_find_by is not None:
            bug_dict['bug_find_by'] = user_find_by.username
        project_name = get_project_by_id(self, bug.bug_project_id)
        if project_name is not None:
            bug_dict['bug_project_id'] = project_name.project_name
        comp_name = get_project_by_id(self, bug.bug_component)
        if comp_name is not None:
            bug_dict['bug_component'] = comp_name.project_name
        result.append(bug_dict)
    return result


class BugTrackHandler(BaseHandler):
    @authenticated
    def get(self):
        belongid = self.get_argument("belongid", None)
        compid = self.get_argument("compid", None)
        blevel = self.get_argument("blevel", None)
        weblog.info("%s.", self._request_summary())
        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid, blevel),
                           users=get_user_list(self), projects=get_project_list(self))
        # return self.render('bug/bugtracklist.html', message="", users=get_user_list(self)
        #                    , projects=get_project_list(self), bugs=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_component = int(self.get_argument("bug_component", '-1'))
        component_belong = int(self.get_argument("component_belong", '-1'))
        bug_level = int(self.get_argument("bug_level", '-1'))
        bug_component = None if bug_component < 0 else bug_component
        component_belong = None if component_belong < 0 else component_belong
        bug_level = None if bug_level < 0 else bug_level
        bugtracks = get_bugtrack_list(self, component_belong, bug_component, bug_level)
        weblog.info("%s. %d %d %d", self._request_summary(), bug_component, component_belong, bug_level)

        return self.write(json.dumps(bugtracks))


class BugTrackAddHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtrackadd.html')
        return self.render('bug/bugtrackadd.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track = TblBugTrack()
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().add(bug_track)
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackEditHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid))
        return self.render('bug/bugtrackedit.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self), bug=get_bugtrack_by_id(self, bid))

    @authenticated
    def post(self, bid):
        weblog.info("%s.", self._request_summary())
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bid).first()
        if bug_track is None:
            msg.append(u"获取问题单为空，问题单id={}".format(bid))
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackedit.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackDeleteHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        bug_track = self.mysqldb().query(TblBugTrack).filter_by(comp_id=bid).first()
        bug_track.bug_project_id = -1
        try:
            self.mysqldb().commit()
        except Exception as e:
            weblog.error("delete bug track id={} error. {}".format(bid, e))
            self.mysqldb().rollback()

        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        # coding=utf-8
import json
from database.tbl_project import TblProject
from database.tbl_bug_list import TblBugList
from database.tbl_account import TblAccount
from database.tbl_bug_track import TblBugTrack
from database.tbl_project_user import TblPorjectUser
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
from tornado.log import access_log as weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord
from handlers.user_manage_handler import get_user_list, get_user_by_id
from handlers.Project.project_manage_handler import get_project_list, get_project_by_id


def get_bugtrack_list(self, belongid=None, compid=None, level=None):
    bugs = self.mysqldb().query(TblBugTrack)
    if belongid is not None:
        bugs = bugs.filter(TblBugTrack.component_belong == belongid)
    if compid is not None:
        bugs = bugs.filter(TblBugTrack.bug_component == compid)
    if level is not None:
        bugs = bugs.filter(TblBugTrack.bug_level == level)
    bugs = bugs.filter(TblBugTrack.bug_project_id > 0)
    bugs = bugs.order_by(TblBugTrack.bug_date_receive.desc())
    bugs = bugs.all()
    # for project in projects:
    #     print(project.describe,type(project.describe))
    result = gene_bugtrack_result(self, bugs)
    return result


def get_bugtrack_by_id(self, bug_id):
    bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bug_id).first()
    result = gene_bugtrack_result(self, [bug_track])
    if result:
        return result[0]
    else:
        return []


def gene_bugtrack_result(self, bugs):
    result = []
    for bug in bugs:
        bug_dict = dict()
        bug_dict['bug_id'] = bug.bug_id
        bug_dict['bug_date_receive'] = str(bug.bug_date_receive)
        bug_dict['bug_find_by'] = bug.bug_find_by
        bug_dict['bug_component'] = bug.bug_component
        bug_dict['component_belong'] = bug.component_belong
        bug_dict['component_community'] = bug.component_community
        bug_dict['bug_project_id'] = bug.bug_project_id
        bug_dict['project_version'] = bug.project_version
        bug_dict['bug_describe'] = bug.bug_describe
        bug_dict['bug_level'] = msg_define.BUG_LEVEL[bug.bug_level]
        bug_dict['bug_reason'] = bug.bug_reason
        bug_dict['bug_solution'] = bug.bug_solution
        bug_dict['bug_progress'] = bug.bug_progress
        bug_dict['bug_date_plan'] = str(bug.bug_date_plan)
        bug_dict['bug_date_done'] = str(bug.bug_date_done)
        bug_dict['bug_user_done'] = bug.bug_user_done
        bug_dict['bug_version'] = bug.bug_version
        user = get_user_by_id(self, bug.bug_user_done)
        if user is not None:
            bug_dict['bug_user_done'] = user.username
        user_comp_belong = get_user_by_id(self, bug.component_belong)
        if user_comp_belong is not None:
            bug_dict['component_belong'] = user_comp_belong.username
        user_find_by = get_user_by_id(self, bug.bug_find_by)
        if user_find_by is not None:
            bug_dict['bug_find_by'] = user_find_by.username
        project_name = get_project_by_id(self, bug.bug_project_id)
        if project_name is not None:
            bug_dict['bug_project_id'] = project_name.project_name
        comp_name = get_project_by_id(self, bug.bug_component)
        if comp_name is not None:
            bug_dict['bug_component'] = comp_name.project_name
        result.append(bug_dict)
    return result


class BugTrackHandler(BaseHandler):
    @authenticated
    def get(self):
        belongid = self.get_argument("belongid", None)
        compid = self.get_argument("compid", None)
        blevel = self.get_argument("blevel", None)
        weblog.info("%s.", self._request_summary())
        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid, blevel),
                           users=get_user_list(self), projects=get_project_list(self))
        # return self.render('bug/bugtracklist.html', message="", users=get_user_list(self)
        #                    , projects=get_project_list(self), bugs=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_component = int(self.get_argument("bug_component", '-1'))
        component_belong = int(self.get_argument("component_belong", '-1'))
        bug_level = int(self.get_argument("bug_level", '-1'))
        bug_component = None if bug_component < 0 else bug_component
        component_belong = None if component_belong < 0 else component_belong
        bug_level = None if bug_level < 0 else bug_level
        bugtracks = get_bugtrack_list(self, component_belong, bug_component, bug_level)
        weblog.info("%s. %d %d %d", self._request_summary(), bug_component, component_belong, bug_level)

        return self.write(json.dumps(bugtracks))


class BugTrackAddHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtrackadd.html')
        return self.render('bug/bugtrackadd.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track = TblBugTrack()
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().add(bug_track)
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackEditHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid))
        return self.render('bug/bugtrackedit.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self), bug=get_bugtrack_by_id(self, bid))

    @authenticated
    def post(self, bid):
        weblog.info("%s.", self._request_summary())
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bid).first()
        if bug_track is None:
            msg.append(u"获取问题单为空，问题单id={}".format(bid))
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackedit.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackDeleteHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        bug_track = self.mysqldb().query(TblBugTrack).filter_by(comp_id=bid).first()
        bug_track.bug_project_id = -1
        try:
            self.mysqldb().commit()
        except Exception as e:
            weblog.error("delete bug track id={} error. {}".format(bid, e))
            self.mysqldb().rollback()

        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        # coding=utf-8
import json
from database.tbl_project import TblProject
from database.tbl_bug_list import TblBugList
from database.tbl_account import TblAccount
from database.tbl_bug_track import TblBugTrack
from database.tbl_project_user import TblPorjectUser
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
from tornado.log import access_log as weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord
from handlers.user_manage_handler import get_user_list, get_user_by_id
from handlers.Project.project_manage_handler import get_project_list, get_project_by_id


def get_bugtrack_list(self, belongid=None, compid=None, level=None):
    bugs = self.mysqldb().query(TblBugTrack)
    if belongid is not None:
        bugs = bugs.filter(TblBugTrack.component_belong == belongid)
    if compid is not None:
        bugs = bugs.filter(TblBugTrack.bug_component == compid)
    if level is not None:
        bugs = bugs.filter(TblBugTrack.bug_level == level)
    bugs = bugs.filter(TblBugTrack.bug_project_id > 0)
    bugs = bugs.order_by(TblBugTrack.bug_date_receive.desc())
    bugs = bugs.all()
    # for project in projects:
    #     print(project.describe,type(project.describe))
    result = gene_bugtrack_result(self, bugs)
    return result


def get_bugtrack_by_id(self, bug_id):
    bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bug_id).first()
    result = gene_bugtrack_result(self, [bug_track])
    if result:
        return result[0]
    else:
        return []


def gene_bugtrack_result(self, bugs):
    result = []
    for bug in bugs:
        bug_dict = dict()
        bug_dict['bug_id'] = bug.bug_id
        bug_dict['bug_date_receive'] = str(bug.bug_date_receive)
        bug_dict['bug_find_by'] = bug.bug_find_by
        bug_dict['bug_component'] = bug.bug_component
        bug_dict['component_belong'] = bug.component_belong
        bug_dict['component_community'] = bug.component_community
        bug_dict['bug_project_id'] = bug.bug_project_id
        bug_dict['project_version'] = bug.project_version
        bug_dict['bug_describe'] = bug.bug_describe
        bug_dict['bug_level'] = msg_define.BUG_LEVEL[bug.bug_level]
        bug_dict['bug_reason'] = bug.bug_reason
        bug_dict['bug_solution'] = bug.bug_solution
        bug_dict['bug_progress'] = bug.bug_progress
        bug_dict['bug_date_plan'] = str(bug.bug_date_plan)
        bug_dict['bug_date_done'] = str(bug.bug_date_done)
        bug_dict['bug_user_done'] = bug.bug_user_done
        bug_dict['bug_version'] = bug.bug_version
        user = get_user_by_id(self, bug.bug_user_done)
        if user is not None:
            bug_dict['bug_user_done'] = user.username
        user_comp_belong = get_user_by_id(self, bug.component_belong)
        if user_comp_belong is not None:
            bug_dict['component_belong'] = user_comp_belong.username
        user_find_by = get_user_by_id(self, bug.bug_find_by)
        if user_find_by is not None:
            bug_dict['bug_find_by'] = user_find_by.username
        project_name = get_project_by_id(self, bug.bug_project_id)
        if project_name is not None:
            bug_dict['bug_project_id'] = project_name.project_name
        comp_name = get_project_by_id(self, bug.bug_component)
        if comp_name is not None:
            bug_dict['bug_component'] = comp_name.project_name
        result.append(bug_dict)
    return result


class BugTrackHandler(BaseHandler):
    @authenticated
    def get(self):
        belongid = self.get_argument("belongid", None)
        compid = self.get_argument("compid", None)
        blevel = self.get_argument("blevel", None)
        weblog.info("%s.", self._request_summary())
        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid, blevel),
                           users=get_user_list(self), projects=get_project_list(self))
        # return self.render('bug/bugtracklist.html', message="", users=get_user_list(self)
        #                    , projects=get_project_list(self), bugs=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_component = int(self.get_argument("bug_component", '-1'))
        component_belong = int(self.get_argument("component_belong", '-1'))
        bug_level = int(self.get_argument("bug_level", '-1'))
        bug_component = None if bug_component < 0 else bug_component
        component_belong = None if component_belong < 0 else component_belong
        bug_level = None if bug_level < 0 else bug_level
        bugtracks = get_bugtrack_list(self, component_belong, bug_component, bug_level)
        weblog.info("%s. %d %d %d", self._request_summary(), bug_component, component_belong, bug_level)

        return self.write(json.dumps(bugtracks))


class BugTrackAddHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtrackadd.html')
        return self.render('bug/bugtrackadd.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track = TblBugTrack()
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().add(bug_track)
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackEditHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid))
        return self.render('bug/bugtrackedit.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self), bug=get_bugtrack_by_id(self, bid))

    @authenticated
    def post(self, bid):
        weblog.info("%s.", self._request_summary())
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bid).first()
        if bug_track is None:
            msg.append(u"获取问题单为空，问题单id={}".format(bid))
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackedit.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackDeleteHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        bug_track = self.mysqldb().query(TblBugTrack).filter_by(comp_id=bid).first()
        bug_track.bug_project_id = -1
        try:
            self.mysqldb().commit()
        except Exception as e:
            weblog.error("delete bug track id={} error. {}".format(bid, e))
            self.mysqldb().rollback()

        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        # coding=utf-8
import json
from database.tbl_project import TblProject
from database.tbl_bug_list import TblBugList
from database.tbl_account import TblAccount
from database.tbl_bug_track import TblBugTrack
from database.tbl_project_user import TblPorjectUser
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
from tornado.log import access_log as weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord
from handlers.user_manage_handler import get_user_list, get_user_by_id
from handlers.Project.project_manage_handler import get_project_list, get_project_by_id


def get_bugtrack_list(self, belongid=None, compid=None, level=None):
    bugs = self.mysqldb().query(TblBugTrack)
    if belongid is not None:
        bugs = bugs.filter(TblBugTrack.component_belong == belongid)
    if compid is not None:
        bugs = bugs.filter(TblBugTrack.bug_component == compid)
    if level is not None:
        bugs = bugs.filter(TblBugTrack.bug_level == level)
    bugs = bugs.filter(TblBugTrack.bug_project_id > 0)
    bugs = bugs.order_by(TblBugTrack.bug_date_receive.desc())
    bugs = bugs.all()
    # for project in projects:
    #     print(project.describe,type(project.describe))
    result = gene_bugtrack_result(self, bugs)
    return result


def get_bugtrack_by_id(self, bug_id):
    bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bug_id).first()
    result = gene_bugtrack_result(self, [bug_track])
    if result:
        return result[0]
    else:
        return []


def gene_bugtrack_result(self, bugs):
    result = []
    for bug in bugs:
        bug_dict = dict()
        bug_dict['bug_id'] = bug.bug_id
        bug_dict['bug_date_receive'] = str(bug.bug_date_receive)
        bug_dict['bug_find_by'] = bug.bug_find_by
        bug_dict['bug_component'] = bug.bug_component
        bug_dict['component_belong'] = bug.component_belong
        bug_dict['component_community'] = bug.component_community
        bug_dict['bug_project_id'] = bug.bug_project_id
        bug_dict['project_version'] = bug.project_version
        bug_dict['bug_describe'] = bug.bug_describe
        bug_dict['bug_level'] = msg_define.BUG_LEVEL[bug.bug_level]
        bug_dict['bug_reason'] = bug.bug_reason
        bug_dict['bug_solution'] = bug.bug_solution
        bug_dict['bug_progress'] = bug.bug_progress
        bug_dict['bug_date_plan'] = str(bug.bug_date_plan)
        bug_dict['bug_date_done'] = str(bug.bug_date_done)
        bug_dict['bug_user_done'] = bug.bug_user_done
        bug_dict['bug_version'] = bug.bug_version
        user = get_user_by_id(self, bug.bug_user_done)
        if user is not None:
            bug_dict['bug_user_done'] = user.username
        user_comp_belong = get_user_by_id(self, bug.component_belong)
        if user_comp_belong is not None:
            bug_dict['component_belong'] = user_comp_belong.username
        user_find_by = get_user_by_id(self, bug.bug_find_by)
        if user_find_by is not None:
            bug_dict['bug_find_by'] = user_find_by.username
        project_name = get_project_by_id(self, bug.bug_project_id)
        if project_name is not None:
            bug_dict['bug_project_id'] = project_name.project_name
        comp_name = get_project_by_id(self, bug.bug_component)
        if comp_name is not None:
            bug_dict['bug_component'] = comp_name.project_name
        result.append(bug_dict)
    return result


class BugTrackHandler(BaseHandler):
    @authenticated
    def get(self):
        belongid = self.get_argument("belongid", None)
        compid = self.get_argument("compid", None)
        blevel = self.get_argument("blevel", None)
        weblog.info("%s.", self._request_summary())
        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid, blevel),
                           users=get_user_list(self), projects=get_project_list(self))
        # return self.render('bug/bugtracklist.html', message="", users=get_user_list(self)
        #                    , projects=get_project_list(self), bugs=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_component = int(self.get_argument("bug_component", '-1'))
        component_belong = int(self.get_argument("component_belong", '-1'))
        bug_level = int(self.get_argument("bug_level", '-1'))
        bug_component = None if bug_component < 0 else bug_component
        component_belong = None if component_belong < 0 else component_belong
        bug_level = None if bug_level < 0 else bug_level
        bugtracks = get_bugtrack_list(self, component_belong, bug_component, bug_level)
        weblog.info("%s. %d %d %d", self._request_summary(), bug_component, component_belong, bug_level)

        return self.write(json.dumps(bugtracks))


class BugTrackAddHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtrackadd.html')
        return self.render('bug/bugtrackadd.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track = TblBugTrack()
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().add(bug_track)
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackEditHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid))
        return self.render('bug/bugtrackedit.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self), bug=get_bugtrack_by_id(self, bid))

    @authenticated
    def post(self, bid):
        weblog.info("%s.", self._request_summary())
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bid).first()
        if bug_track is None:
            msg.append(u"获取问题单为空，问题单id={}".format(bid))
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackedit.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackDeleteHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        bug_track = self.mysqldb().query(TblBugTrack).filter_by(comp_id=bid).first()
        bug_track.bug_project_id = -1
        try:
            self.mysqldb().commit()
        except Exception as e:
            weblog.error("delete bug track id={} error. {}".format(bid, e))
            self.mysqldb().rollback()

        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        # coding=utf-8
import json
from database.tbl_project import TblProject
from database.tbl_bug_list import TblBugList
from database.tbl_account import TblAccount
from database.tbl_bug_track import TblBugTrack
from database.tbl_project_user import TblPorjectUser
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
from tornado.log import access_log as weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord
from handlers.user_manage_handler import get_user_list, get_user_by_id
from handlers.Project.project_manage_handler import get_project_list, get_project_by_id


def get_bugtrack_list(self, belongid=None, compid=None, level=None):
    bugs = self.mysqldb().query(TblBugTrack)
    if belongid is not None:
        bugs = bugs.filter(TblBugTrack.component_belong == belongid)
    if compid is not None:
        bugs = bugs.filter(TblBugTrack.bug_component == compid)
    if level is not None:
        bugs = bugs.filter(TblBugTrack.bug_level == level)
    bugs = bugs.filter(TblBugTrack.bug_project_id > 0)
    bugs = bugs.order_by(TblBugTrack.bug_date_receive.desc())
    bugs = bugs.all()
    # for project in projects:
    #     print(project.describe,type(project.describe))
    result = gene_bugtrack_result(self, bugs)
    return result


def get_bugtrack_by_id(self, bug_id):
    bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bug_id).first()
    result = gene_bugtrack_result(self, [bug_track])
    if result:
        return result[0]
    else:
        return []


def gene_bugtrack_result(self, bugs):
    result = []
    for bug in bugs:
        bug_dict = dict()
        bug_dict['bug_id'] = bug.bug_id
        bug_dict['bug_date_receive'] = str(bug.bug_date_receive)
        bug_dict['bug_find_by'] = bug.bug_find_by
        bug_dict['bug_component'] = bug.bug_component
        bug_dict['component_belong'] = bug.component_belong
        bug_dict['component_community'] = bug.component_community
        bug_dict['bug_project_id'] = bug.bug_project_id
        bug_dict['project_version'] = bug.project_version
        bug_dict['bug_describe'] = bug.bug_describe
        bug_dict['bug_level'] = msg_define.BUG_LEVEL[bug.bug_level]
        bug_dict['bug_reason'] = bug.bug_reason
        bug_dict['bug_solution'] = bug.bug_solution
        bug_dict['bug_progress'] = bug.bug_progress
        bug_dict['bug_date_plan'] = str(bug.bug_date_plan)
        bug_dict['bug_date_done'] = str(bug.bug_date_done)
        bug_dict['bug_user_done'] = bug.bug_user_done
        bug_dict['bug_version'] = bug.bug_version
        user = get_user_by_id(self, bug.bug_user_done)
        if user is not None:
            bug_dict['bug_user_done'] = user.username
        user_comp_belong = get_user_by_id(self, bug.component_belong)
        if user_comp_belong is not None:
            bug_dict['component_belong'] = user_comp_belong.username
        user_find_by = get_user_by_id(self, bug.bug_find_by)
        if user_find_by is not None:
            bug_dict['bug_find_by'] = user_find_by.username
        project_name = get_project_by_id(self, bug.bug_project_id)
        if project_name is not None:
            bug_dict['bug_project_id'] = project_name.project_name
        comp_name = get_project_by_id(self, bug.bug_component)
        if comp_name is not None:
            bug_dict['bug_component'] = comp_name.project_name
        result.append(bug_dict)
    return result


class BugTrackHandler(BaseHandler):
    @authenticated
    def get(self):
        belongid = self.get_argument("belongid", None)
        compid = self.get_argument("compid", None)
        blevel = self.get_argument("blevel", None)
        weblog.info("%s.", self._request_summary())
        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid, blevel),
                           users=get_user_list(self), projects=get_project_list(self))
        # return self.render('bug/bugtracklist.html', message="", users=get_user_list(self)
        #                    , projects=get_project_list(self), bugs=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_component = int(self.get_argument("bug_component", '-1'))
        component_belong = int(self.get_argument("component_belong", '-1'))
        bug_level = int(self.get_argument("bug_level", '-1'))
        bug_component = None if bug_component < 0 else bug_component
        component_belong = None if component_belong < 0 else component_belong
        bug_level = None if bug_level < 0 else bug_level
        bugtracks = get_bugtrack_list(self, component_belong, bug_component, bug_level)
        weblog.info("%s. %d %d %d", self._request_summary(), bug_component, component_belong, bug_level)

        return self.write(json.dumps(bugtracks))


class BugTrackAddHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtrackadd.html')
        return self.render('bug/bugtrackadd.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track = TblBugTrack()
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().add(bug_track)
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackEditHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid))
        return self.render('bug/bugtrackedit.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self), bug=get_bugtrack_by_id(self, bid))

    @authenticated
    def post(self, bid):
        weblog.info("%s.", self._request_summary())
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bid).first()
        if bug_track is None:
            msg.append(u"获取问题单为空，问题单id={}".format(bid))
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackedit.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackDeleteHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        bug_track = self.mysqldb().query(TblBugTrack).filter_by(comp_id=bid).first()
        bug_track.bug_project_id = -1
        try:
            self.mysqldb().commit()
        except Exception as e:
            weblog.error("delete bug track id={} error. {}".format(bid, e))
            self.mysqldb().rollback()

        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        # coding=utf-8
import json
from database.tbl_project import TblProject
from database.tbl_bug_list import TblBugList
from database.tbl_account import TblAccount
from database.tbl_bug_track import TblBugTrack
from database.tbl_project_user import TblPorjectUser
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
from tornado.log import access_log as weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord
from handlers.user_manage_handler import get_user_list, get_user_by_id
from handlers.Project.project_manage_handler import get_project_list, get_project_by_id


def get_bugtrack_list(self, belongid=None, compid=None, level=None):
    bugs = self.mysqldb().query(TblBugTrack)
    if belongid is not None:
        bugs = bugs.filter(TblBugTrack.component_belong == belongid)
    if compid is not None:
        bugs = bugs.filter(TblBugTrack.bug_component == compid)
    if level is not None:
        bugs = bugs.filter(TblBugTrack.bug_level == level)
    bugs = bugs.filter(TblBugTrack.bug_project_id > 0)
    bugs = bugs.order_by(TblBugTrack.bug_date_receive.desc())
    bugs = bugs.all()
    # for project in projects:
    #     print(project.describe,type(project.describe))
    result = gene_bugtrack_result(self, bugs)
    return result


def get_bugtrack_by_id(self, bug_id):
    bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bug_id).first()
    result = gene_bugtrack_result(self, [bug_track])
    if result:
        return result[0]
    else:
        return []


def gene_bugtrack_result(self, bugs):
    result = []
    for bug in bugs:
        bug_dict = dict()
        bug_dict['bug_id'] = bug.bug_id
        bug_dict['bug_date_receive'] = str(bug.bug_date_receive)
        bug_dict['bug_find_by'] = bug.bug_find_by
        bug_dict['bug_component'] = bug.bug_component
        bug_dict['component_belong'] = bug.component_belong
        bug_dict['component_community'] = bug.component_community
        bug_dict['bug_project_id'] = bug.bug_project_id
        bug_dict['project_version'] = bug.project_version
        bug_dict['bug_describe'] = bug.bug_describe
        bug_dict['bug_level'] = msg_define.BUG_LEVEL[bug.bug_level]
        bug_dict['bug_reason'] = bug.bug_reason
        bug_dict['bug_solution'] = bug.bug_solution
        bug_dict['bug_progress'] = bug.bug_progress
        bug_dict['bug_date_plan'] = str(bug.bug_date_plan)
        bug_dict['bug_date_done'] = str(bug.bug_date_done)
        bug_dict['bug_user_done'] = bug.bug_user_done
        bug_dict['bug_version'] = bug.bug_version
        user = get_user_by_id(self, bug.bug_user_done)
        if user is not None:
            bug_dict['bug_user_done'] = user.username
        user_comp_belong = get_user_by_id(self, bug.component_belong)
        if user_comp_belong is not None:
            bug_dict['component_belong'] = user_comp_belong.username
        user_find_by = get_user_by_id(self, bug.bug_find_by)
        if user_find_by is not None:
            bug_dict['bug_find_by'] = user_find_by.username
        project_name = get_project_by_id(self, bug.bug_project_id)
        if project_name is not None:
            bug_dict['bug_project_id'] = project_name.project_name
        comp_name = get_project_by_id(self, bug.bug_component)
        if comp_name is not None:
            bug_dict['bug_component'] = comp_name.project_name
        result.append(bug_dict)
    return result


class BugTrackHandler(BaseHandler):
    @authenticated
    def get(self):
        belongid = self.get_argument("belongid", None)
        compid = self.get_argument("compid", None)
        blevel = self.get_argument("blevel", None)
        weblog.info("%s.", self._request_summary())
        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid, blevel),
                           users=get_user_list(self), projects=get_project_list(self))
        # return self.render('bug/bugtracklist.html', message="", users=get_user_list(self)
        #                    , projects=get_project_list(self), bugs=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_component = int(self.get_argument("bug_component", '-1'))
        component_belong = int(self.get_argument("component_belong", '-1'))
        bug_level = int(self.get_argument("bug_level", '-1'))
        bug_component = None if bug_component < 0 else bug_component
        component_belong = None if component_belong < 0 else component_belong
        bug_level = None if bug_level < 0 else bug_level
        bugtracks = get_bugtrack_list(self, component_belong, bug_component, bug_level)
        weblog.info("%s. %d %d %d", self._request_summary(), bug_component, component_belong, bug_level)

        return self.write(json.dumps(bugtracks))


class BugTrackAddHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtrackadd.html')
        return self.render('bug/bugtrackadd.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track = TblBugTrack()
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().add(bug_track)
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackEditHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid))
        return self.render('bug/bugtrackedit.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self), bug=get_bugtrack_by_id(self, bid))

    @authenticated
    def post(self, bid):
        weblog.info("%s.", self._request_summary())
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bid).first()
        if bug_track is None:
            msg.append(u"获取问题单为空，问题单id={}".format(bid))
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackedit.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackDeleteHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        bug_track = self.mysqldb().query(TblBugTrack).filter_by(comp_id=bid).first()
        bug_track.bug_project_id = -1
        try:
            self.mysqldb().commit()
        except Exception as e:
            weblog.error("delete bug track id={} error. {}".format(bid, e))
            self.mysqldb().rollback()

        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())


        # coding=utf-8
import json
from database.tbl_project import TblProject
from database.tbl_bug_list import TblBugList
from database.tbl_account import TblAccount
from database.tbl_bug_track import TblBugTrack
from database.tbl_project_user import TblPorjectUser
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
from tornado.log import access_log as weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord
from handlers.user_manage_handler import get_user_list, get_user_by_id
from handlers.Project.project_manage_handler import get_project_list, get_project_by_id


def get_bugtrack_list(self, belongid=None, compid=None, level=None):
    bugs = self.mysqldb().query(TblBugTrack)
    if belongid is not None:
        bugs = bugs.filter(TblBugTrack.component_belong == belongid)
    if compid is not None:
        bugs = bugs.filter(TblBugTrack.bug_component == compid)
    if level is not None:
        bugs = bugs.filter(TblBugTrack.bug_level == level)
    bugs = bugs.filter(TblBugTrack.bug_project_id > 0)
    bugs = bugs.order_by(TblBugTrack.bug_date_receive.desc())
    bugs = bugs.all()
    # for project in projects:
    #     print(project.describe,type(project.describe))
    result = gene_bugtrack_result(self, bugs)
    return result


def get_bugtrack_by_id(self, bug_id):
    bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bug_id).first()
    result = gene_bugtrack_result(self, [bug_track])
    if result:
        return result[0]
    else:
        return []


def gene_bugtrack_result(self, bugs):
    result = []
    for bug in bugs:
        bug_dict = dict()
        bug_dict['bug_id'] = bug.bug_id
        bug_dict['bug_date_receive'] = str(bug.bug_date_receive)
        bug_dict['bug_find_by'] = bug.bug_find_by
        bug_dict['bug_component'] = bug.bug_component
        bug_dict['component_belong'] = bug.component_belong
        bug_dict['component_community'] = bug.component_community
        bug_dict['bug_project_id'] = bug.bug_project_id
        bug_dict['project_version'] = bug.project_version
        bug_dict['bug_describe'] = bug.bug_describe
        bug_dict['bug_level'] = msg_define.BUG_LEVEL[bug.bug_level]
        bug_dict['bug_reason'] = bug.bug_reason
        bug_dict['bug_solution'] = bug.bug_solution
        bug_dict['bug_progress'] = bug.bug_progress
        bug_dict['bug_date_plan'] = str(bug.bug_date_plan)
        bug_dict['bug_date_done'] = str(bug.bug_date_done)
        bug_dict['bug_user_done'] = bug.bug_user_done
        bug_dict['bug_version'] = bug.bug_version
        user = get_user_by_id(self, bug.bug_user_done)
        if user is not None:
            bug_dict['bug_user_done'] = user.username
        user_comp_belong = get_user_by_id(self, bug.component_belong)
        if user_comp_belong is not None:
            bug_dict['component_belong'] = user_comp_belong.username
        user_find_by = get_user_by_id(self, bug.bug_find_by)
        if user_find_by is not None:
            bug_dict['bug_find_by'] = user_find_by.username
        project_name = get_project_by_id(self, bug.bug_project_id)
        if project_name is not None:
            bug_dict['bug_project_id'] = project_name.project_name
        comp_name = get_project_by_id(self, bug.bug_component)
        if comp_name is not None:
            bug_dict['bug_component'] = comp_name.project_name
        result.append(bug_dict)
    return result


class BugTrackHandler(BaseHandler):
    @authenticated
    def get(self):
        belongid = self.get_argument("belongid", None)
        compid = self.get_argument("compid", None)
        blevel = self.get_argument("blevel", None)
        weblog.info("%s.", self._request_summary())
        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid, blevel),
                           users=get_user_list(self), projects=get_project_list(self))
        # return self.render('bug/bugtracklist.html', message="", users=get_user_list(self)
        #                    , projects=get_project_list(self), bugs=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_component = int(self.get_argument("bug_component", '-1'))
        component_belong = int(self.get_argument("component_belong", '-1'))
        bug_level = int(self.get_argument("bug_level", '-1'))
        bug_component = None if bug_component < 0 else bug_component
        component_belong = None if component_belong < 0 else component_belong
        bug_level = None if bug_level < 0 else bug_level
        bugtracks = get_bugtrack_list(self, component_belong, bug_component, bug_level)
        weblog.info("%s. %d %d %d", self._request_summary(), bug_component, component_belong, bug_level)

        return self.write(json.dumps(bugtracks))


class BugTrackAddHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtrackadd.html')
        return self.render('bug/bugtrackadd.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track = TblBugTrack()
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().add(bug_track)
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackEditHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid))
        return self.render('bug/bugtrackedit.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self), bug=get_bugtrack_by_id(self, bid))

    @authenticated
    def post(self, bid):
        weblog.info("%s.", self._request_summary())
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bid).first()
        if bug_track is None:
            msg.append(u"获取问题单为空，问题单id={}".format(bid))
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackedit.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackDeleteHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        bug_track = self.mysqldb().query(TblBugTrack).filter_by(comp_id=bid).first()
        bug_track.bug_project_id = -1
        try:
            self.mysqldb().commit()
        except Exception as e:
            weblog.error("delete bug track id={} error. {}".format(bid, e))
            self.mysqldb().rollback()

        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        # coding=utf-8
import json
from database.tbl_project import TblProject
from database.tbl_bug_list import TblBugList
from database.tbl_account import TblAccount
from database.tbl_bug_track import TblBugTrack
from database.tbl_project_user import TblPorjectUser
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
from tornado.log import access_log as weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord
from handlers.user_manage_handler import get_user_list, get_user_by_id
from handlers.Project.project_manage_handler import get_project_list, get_project_by_id


def get_bugtrack_list(self, belongid=None, compid=None, level=None):
    bugs = self.mysqldb().query(TblBugTrack)
    if belongid is not None:
        bugs = bugs.filter(TblBugTrack.component_belong == belongid)
    if compid is not None:
        bugs = bugs.filter(TblBugTrack.bug_component == compid)
    if level is not None:
        bugs = bugs.filter(TblBugTrack.bug_level == level)
    bugs = bugs.filter(TblBugTrack.bug_project_id > 0)
    bugs = bugs.order_by(TblBugTrack.bug_date_receive.desc())
    bugs = bugs.all()
    # for project in projects:
    #     print(project.describe,type(project.describe))
    result = gene_bugtrack_result(self, bugs)
    return result


def get_bugtrack_by_id(self, bug_id):
    bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bug_id).first()
    result = gene_bugtrack_result(self, [bug_track])
    if result:
        return result[0]
    else:
        return []


def gene_bugtrack_result(self, bugs):
    result = []
    for bug in bugs:
        bug_dict = dict()
        bug_dict['bug_id'] = bug.bug_id
        bug_dict['bug_date_receive'] = str(bug.bug_date_receive)
        bug_dict['bug_find_by'] = bug.bug_find_by
        bug_dict['bug_component'] = bug.bug_component
        bug_dict['component_belong'] = bug.component_belong
        bug_dict['component_community'] = bug.component_community
        bug_dict['bug_project_id'] = bug.bug_project_id
        bug_dict['project_version'] = bug.project_version
        bug_dict['bug_describe'] = bug.bug_describe
        bug_dict['bug_level'] = msg_define.BUG_LEVEL[bug.bug_level]
        bug_dict['bug_reason'] = bug.bug_reason
        bug_dict['bug_solution'] = bug.bug_solution
        bug_dict['bug_progress'] = bug.bug_progress
        bug_dict['bug_date_plan'] = str(bug.bug_date_plan)
        bug_dict['bug_date_done'] = str(bug.bug_date_done)
        bug_dict['bug_user_done'] = bug.bug_user_done
        bug_dict['bug_version'] = bug.bug_version
        user = get_user_by_id(self, bug.bug_user_done)
        if user is not None:
            bug_dict['bug_user_done'] = user.username
        user_comp_belong = get_user_by_id(self, bug.component_belong)
        if user_comp_belong is not None:
            bug_dict['component_belong'] = user_comp_belong.username
        user_find_by = get_user_by_id(self, bug.bug_find_by)
        if user_find_by is not None:
            bug_dict['bug_find_by'] = user_find_by.username
        project_name = get_project_by_id(self, bug.bug_project_id)
        if project_name is not None:
            bug_dict['bug_project_id'] = project_name.project_name
        comp_name = get_project_by_id(self, bug.bug_component)
        if comp_name is not None:
            bug_dict['bug_component'] = comp_name.project_name
        result.append(bug_dict)
    return result


class BugTrackHandler(BaseHandler):
    @authenticated
    def get(self):
        belongid = self.get_argument("belongid", None)
        compid = self.get_argument("compid", None)
        blevel = self.get_argument("blevel", None)
        weblog.info("%s.", self._request_summary())
        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid, blevel),
                           users=get_user_list(self), projects=get_project_list(self))
        # return self.render('bug/bugtracklist.html', message="", users=get_user_list(self)
        #                    , projects=get_project_list(self), bugs=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_component = int(self.get_argument("bug_component", '-1'))
        component_belong = int(self.get_argument("component_belong", '-1'))
        bug_level = int(self.get_argument("bug_level", '-1'))
        bug_component = None if bug_component < 0 else bug_component
        component_belong = None if component_belong < 0 else component_belong
        bug_level = None if bug_level < 0 else bug_level
        bugtracks = get_bugtrack_list(self, component_belong, bug_component, bug_level)
        weblog.info("%s. %d %d %d", self._request_summary(), bug_component, component_belong, bug_level)

        return self.write(json.dumps(bugtracks))


class BugTrackAddHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtrackadd.html')
        return self.render('bug/bugtrackadd.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track = TblBugTrack()
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().add(bug_track)
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackEditHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid))
        return self.render('bug/bugtrackedit.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self), bug=get_bugtrack_by_id(self, bid))

    @authenticated
    def post(self, bid):
        weblog.info("%s.", self._request_summary())
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bid).first()
        if bug_track is None:
            msg.append(u"获取问题单为空，问题单id={}".format(bid))
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackedit.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackDeleteHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        bug_track = self.mysqldb().query(TblBugTrack).filter_by(comp_id=bid).first()
        bug_track.bug_project_id = -1
        try:
            self.mysqldb().commit()
        except Exception as e:
            weblog.error("delete bug track id={} error. {}".format(bid, e))
            self.mysqldb().rollback()

        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        # coding=utf-8
import json
from database.tbl_project import TblProject
from database.tbl_bug_list import TblBugList
from database.tbl_account import TblAccount
from database.tbl_bug_track import TblBugTrack
from database.tbl_project_user import TblPorjectUser
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
from tornado.log import access_log as weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord
from handlers.user_manage_handler import get_user_list, get_user_by_id
from handlers.Project.project_manage_handler import get_project_list, get_project_by_id


def get_bugtrack_list(self, belongid=None, compid=None, level=None):
    bugs = self.mysqldb().query(TblBugTrack)
    if belongid is not None:
        bugs = bugs.filter(TblBugTrack.component_belong == belongid)
    if compid is not None:
        bugs = bugs.filter(TblBugTrack.bug_component == compid)
    if level is not None:
        bugs = bugs.filter(TblBugTrack.bug_level == level)
    bugs = bugs.filter(TblBugTrack.bug_project_id > 0)
    bugs = bugs.order_by(TblBugTrack.bug_date_receive.desc())
    bugs = bugs.all()
    # for project in projects:
    #     print(project.describe,type(project.describe))
    result = gene_bugtrack_result(self, bugs)
    return result


def get_bugtrack_by_id(self, bug_id):
    bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bug_id).first()
    result = gene_bugtrack_result(self, [bug_track])
    if result:
        return result[0]
    else:
        return []


def gene_bugtrack_result(self, bugs):
    result = []
    for bug in bugs:
        bug_dict = dict()
        bug_dict['bug_id'] = bug.bug_id
        bug_dict['bug_date_receive'] = str(bug.bug_date_receive)
        bug_dict['bug_find_by'] = bug.bug_find_by
        bug_dict['bug_component'] = bug.bug_component
        bug_dict['component_belong'] = bug.component_belong
        bug_dict['component_community'] = bug.component_community
        bug_dict['bug_project_id'] = bug.bug_project_id
        bug_dict['project_version'] = bug.project_version
        bug_dict['bug_describe'] = bug.bug_describe
        bug_dict['bug_level'] = msg_define.BUG_LEVEL[bug.bug_level]
        bug_dict['bug_reason'] = bug.bug_reason
        bug_dict['bug_solution'] = bug.bug_solution
        bug_dict['bug_progress'] = bug.bug_progress
        bug_dict['bug_date_plan'] = str(bug.bug_date_plan)
        bug_dict['bug_date_done'] = str(bug.bug_date_done)
        bug_dict['bug_user_done'] = bug.bug_user_done
        bug_dict['bug_version'] = bug.bug_version
        user = get_user_by_id(self, bug.bug_user_done)
        if user is not None:
            bug_dict['bug_user_done'] = user.username
        user_comp_belong = get_user_by_id(self, bug.component_belong)
        if user_comp_belong is not None:
            bug_dict['component_belong'] = user_comp_belong.username
        user_find_by = get_user_by_id(self, bug.bug_find_by)
        if user_find_by is not None:
            bug_dict['bug_find_by'] = user_find_by.username
        project_name = get_project_by_id(self, bug.bug_project_id)
        if project_name is not None:
            bug_dict['bug_project_id'] = project_name.project_name
        comp_name = get_project_by_id(self, bug.bug_component)
        if comp_name is not None:
            bug_dict['bug_component'] = comp_name.project_name
        result.append(bug_dict)
    return result


class BugTrackHandler(BaseHandler):
    @authenticated
    def get(self):
        belongid = self.get_argument("belongid", None)
        compid = self.get_argument("compid", None)
        blevel = self.get_argument("blevel", None)
        weblog.info("%s.", self._request_summary())
        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid, blevel),
                           users=get_user_list(self), projects=get_project_list(self))
        # return self.render('bug/bugtracklist.html', message="", users=get_user_list(self)
        #                    , projects=get_project_list(self), bugs=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_component = int(self.get_argument("bug_component", '-1'))
        component_belong = int(self.get_argument("component_belong", '-1'))
        bug_level = int(self.get_argument("bug_level", '-1'))
        bug_component = None if bug_component < 0 else bug_component
        component_belong = None if component_belong < 0 else component_belong
        bug_level = None if bug_level < 0 else bug_level
        bugtracks = get_bugtrack_list(self, component_belong, bug_component, bug_level)
        weblog.info("%s. %d %d %d", self._request_summary(), bug_component, component_belong, bug_level)

        return self.write(json.dumps(bugtracks))


class BugTrackAddHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtrackadd.html')
        return self.render('bug/bugtrackadd.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track = TblBugTrack()
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().add(bug_track)
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackEditHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid))
        return self.render('bug/bugtrackedit.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self), bug=get_bugtrack_by_id(self, bid))

    @authenticated
    def post(self, bid):
        weblog.info("%s.", self._request_summary())
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bid).first()
        if bug_track is None:
            msg.append(u"获取问题单为空，问题单id={}".format(bid))
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackedit.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackDeleteHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        bug_track = self.mysqldb().query(TblBugTrack).filter_by(comp_id=bid).first()
        bug_track.bug_project_id = -1
        try:
            self.mysqldb().commit()
        except Exception as e:
            weblog.error("delete bug track id={} error. {}".format(bid, e))
            self.mysqldb().rollback()

        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        # coding=utf-8
import json
from database.tbl_project import TblProject
from database.tbl_bug_list import TblBugList
from database.tbl_account import TblAccount
from database.tbl_bug_track import TblBugTrack
from database.tbl_project_user import TblPorjectUser
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
from tornado.log import access_log as weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord
from handlers.user_manage_handler import get_user_list, get_user_by_id
from handlers.Project.project_manage_handler import get_project_list, get_project_by_id


def get_bugtrack_list(self, belongid=None, compid=None, level=None):
    bugs = self.mysqldb().query(TblBugTrack)
    if belongid is not None:
        bugs = bugs.filter(TblBugTrack.component_belong == belongid)
    if compid is not None:
        bugs = bugs.filter(TblBugTrack.bug_component == compid)
    if level is not None:
        bugs = bugs.filter(TblBugTrack.bug_level == level)
    bugs = bugs.filter(TblBugTrack.bug_project_id > 0)
    bugs = bugs.order_by(TblBugTrack.bug_date_receive.desc())
    bugs = bugs.all()
    # for project in projects:
    #     print(project.describe,type(project.describe))
    result = gene_bugtrack_result(self, bugs)
    return result


def get_bugtrack_by_id(self, bug_id):
    bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bug_id).first()
    result = gene_bugtrack_result(self, [bug_track])
    if result:
        return result[0]
    else:
        return []


def gene_bugtrack_result(self, bugs):
    result = []
    for bug in bugs:
        bug_dict = dict()
        bug_dict['bug_id'] = bug.bug_id
        bug_dict['bug_date_receive'] = str(bug.bug_date_receive)
        bug_dict['bug_find_by'] = bug.bug_find_by
        bug_dict['bug_component'] = bug.bug_component
        bug_dict['component_belong'] = bug.component_belong
        bug_dict['component_community'] = bug.component_community
        bug_dict['bug_project_id'] = bug.bug_project_id
        bug_dict['project_version'] = bug.project_version
        bug_dict['bug_describe'] = bug.bug_describe
        bug_dict['bug_level'] = msg_define.BUG_LEVEL[bug.bug_level]
        bug_dict['bug_reason'] = bug.bug_reason
        bug_dict['bug_solution'] = bug.bug_solution
        bug_dict['bug_progress'] = bug.bug_progress
        bug_dict['bug_date_plan'] = str(bug.bug_date_plan)
        bug_dict['bug_date_done'] = str(bug.bug_date_done)
        bug_dict['bug_user_done'] = bug.bug_user_done
        bug_dict['bug_version'] = bug.bug_version
        user = get_user_by_id(self, bug.bug_user_done)
        if user is not None:
            bug_dict['bug_user_done'] = user.username
        user_comp_belong = get_user_by_id(self, bug.component_belong)
        if user_comp_belong is not None:
            bug_dict['component_belong'] = user_comp_belong.username
        user_find_by = get_user_by_id(self, bug.bug_find_by)
        if user_find_by is not None:
            bug_dict['bug_find_by'] = user_find_by.username
        project_name = get_project_by_id(self, bug.bug_project_id)
        if project_name is not None:
            bug_dict['bug_project_id'] = project_name.project_name
        comp_name = get_project_by_id(self, bug.bug_component)
        if comp_name is not None:
            bug_dict['bug_component'] = comp_name.project_name
        result.append(bug_dict)
    return result


class BugTrackHandler(BaseHandler):
    @authenticated
    def get(self):
        belongid = self.get_argument("belongid", None)
        compid = self.get_argument("compid", None)
        blevel = self.get_argument("blevel", None)
        weblog.info("%s.", self._request_summary())
        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid, blevel),
                           users=get_user_list(self), projects=get_project_list(self))
        # return self.render('bug/bugtracklist.html', message="", users=get_user_list(self)
        #                    , projects=get_project_list(self), bugs=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_component = int(self.get_argument("bug_component", '-1'))
        component_belong = int(self.get_argument("component_belong", '-1'))
        bug_level = int(self.get_argument("bug_level", '-1'))
        bug_component = None if bug_component < 0 else bug_component
        component_belong = None if component_belong < 0 else component_belong
        bug_level = None if bug_level < 0 else bug_level
        bugtracks = get_bugtrack_list(self, component_belong, bug_component, bug_level)
        weblog.info("%s. %d %d %d", self._request_summary(), bug_component, component_belong, bug_level)

        return self.write(json.dumps(bugtracks))


class BugTrackAddHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtrackadd.html')
        return self.render('bug/bugtrackadd.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track = TblBugTrack()
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().add(bug_track)
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackEditHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid))
        return self.render('bug/bugtrackedit.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self), bug=get_bugtrack_by_id(self, bid))

    @authenticated
    def post(self, bid):
        weblog.info("%s.", self._request_summary())
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bid).first()
        if bug_track is None:
            msg.append(u"获取问题单为空，问题单id={}".format(bid))
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackedit.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackDeleteHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        bug_track = self.mysqldb().query(TblBugTrack).filter_by(comp_id=bid).first()
        bug_track.bug_project_id = -1
        try:
            self.mysqldb().commit()
        except Exception as e:
            weblog.error("delete bug track id={} error. {}".format(bid, e))
            self.mysqldb().rollback()

        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        # coding=utf-8
import json
from database.tbl_project import TblProject
from database.tbl_bug_list import TblBugList
from database.tbl_account import TblAccount
from database.tbl_bug_track import TblBugTrack
from database.tbl_project_user import TblPorjectUser
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
from tornado.log import access_log as weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord
from handlers.user_manage_handler import get_user_list, get_user_by_id
from handlers.Project.project_manage_handler import get_project_list, get_project_by_id


def get_bugtrack_list(self, belongid=None, compid=None, level=None):
    bugs = self.mysqldb().query(TblBugTrack)
    if belongid is not None:
        bugs = bugs.filter(TblBugTrack.component_belong == belongid)
    if compid is not None:
        bugs = bugs.filter(TblBugTrack.bug_component == compid)
    if level is not None:
        bugs = bugs.filter(TblBugTrack.bug_level == level)
    bugs = bugs.filter(TblBugTrack.bug_project_id > 0)
    bugs = bugs.order_by(TblBugTrack.bug_date_receive.desc())
    bugs = bugs.all()
    # for project in projects:
    #     print(project.describe,type(project.describe))
    result = gene_bugtrack_result(self, bugs)
    return result


def get_bugtrack_by_id(self, bug_id):
    bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bug_id).first()
    result = gene_bugtrack_result(self, [bug_track])
    if result:
        return result[0]
    else:
        return []


def gene_bugtrack_result(self, bugs):
    result = []
    for bug in bugs:
        bug_dict = dict()
        bug_dict['bug_id'] = bug.bug_id
        bug_dict['bug_date_receive'] = str(bug.bug_date_receive)
        bug_dict['bug_find_by'] = bug.bug_find_by
        bug_dict['bug_component'] = bug.bug_component
        bug_dict['component_belong'] = bug.component_belong
        bug_dict['component_community'] = bug.component_community
        bug_dict['bug_project_id'] = bug.bug_project_id
        bug_dict['project_version'] = bug.project_version
        bug_dict['bug_describe'] = bug.bug_describe
        bug_dict['bug_level'] = msg_define.BUG_LEVEL[bug.bug_level]
        bug_dict['bug_reason'] = bug.bug_reason
        bug_dict['bug_solution'] = bug.bug_solution
        bug_dict['bug_progress'] = bug.bug_progress
        bug_dict['bug_date_plan'] = str(bug.bug_date_plan)
        bug_dict['bug_date_done'] = str(bug.bug_date_done)
        bug_dict['bug_user_done'] = bug.bug_user_done
        bug_dict['bug_version'] = bug.bug_version
        user = get_user_by_id(self, bug.bug_user_done)
        if user is not None:
            bug_dict['bug_user_done'] = user.username
        user_comp_belong = get_user_by_id(self, bug.component_belong)
        if user_comp_belong is not None:
            bug_dict['component_belong'] = user_comp_belong.username
        user_find_by = get_user_by_id(self, bug.bug_find_by)
        if user_find_by is not None:
            bug_dict['bug_find_by'] = user_find_by.username
        project_name = get_project_by_id(self, bug.bug_project_id)
        if project_name is not None:
            bug_dict['bug_project_id'] = project_name.project_name
        comp_name = get_project_by_id(self, bug.bug_component)
        if comp_name is not None:
            bug_dict['bug_component'] = comp_name.project_name
        result.append(bug_dict)
    return result


class BugTrackHandler(BaseHandler):
    @authenticated
    def get(self):
        belongid = self.get_argument("belongid", None)
        compid = self.get_argument("compid", None)
        blevel = self.get_argument("blevel", None)
        weblog.info("%s.", self._request_summary())
        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid, blevel),
                           users=get_user_list(self), projects=get_project_list(self))
        # return self.render('bug/bugtracklist.html', message="", users=get_user_list(self)
        #                    , projects=get_project_list(self), bugs=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_component = int(self.get_argument("bug_component", '-1'))
        component_belong = int(self.get_argument("component_belong", '-1'))
        bug_level = int(self.get_argument("bug_level", '-1'))
        bug_component = None if bug_component < 0 else bug_component
        component_belong = None if component_belong < 0 else component_belong
        bug_level = None if bug_level < 0 else bug_level
        bugtracks = get_bugtrack_list(self, component_belong, bug_component, bug_level)
        weblog.info("%s. %d %d %d", self._request_summary(), bug_component, component_belong, bug_level)

        return self.write(json.dumps(bugtracks))


class BugTrackAddHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtrackadd.html')
        return self.render('bug/bugtrackadd.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track = TblBugTrack()
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().add(bug_track)
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackEditHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid))
        return self.render('bug/bugtrackedit.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self), bug=get_bugtrack_by_id(self, bid))

    @authenticated
    def post(self, bid):
        weblog.info("%s.", self._request_summary())
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bid).first()
        if bug_track is None:
            msg.append(u"获取问题单为空，问题单id={}".format(bid))
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackedit.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackDeleteHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        bug_track = self.mysqldb().query(TblBugTrack).filter_by(comp_id=bid).first()
        bug_track.bug_project_id = -1
        try:
            self.mysqldb().commit()
        except Exception as e:
            weblog.error("delete bug track id={} error. {}".format(bid, e))
            self.mysqldb().rollback()

        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        # coding=utf-8
import json
from database.tbl_project import TblProject
from database.tbl_bug_list import TblBugList
from database.tbl_account import TblAccount
from database.tbl_bug_track import TblBugTrack
from database.tbl_project_user import TblPorjectUser
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
from tornado.log import access_log as weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord
from handlers.user_manage_handler import get_user_list, get_user_by_id
from handlers.Project.project_manage_handler import get_project_list, get_project_by_id


def get_bugtrack_list(self, belongid=None, compid=None, level=None):
    bugs = self.mysqldb().query(TblBugTrack)
    if belongid is not None:
        bugs = bugs.filter(TblBugTrack.component_belong == belongid)
    if compid is not None:
        bugs = bugs.filter(TblBugTrack.bug_component == compid)
    if level is not None:
        bugs = bugs.filter(TblBugTrack.bug_level == level)
    bugs = bugs.filter(TblBugTrack.bug_project_id > 0)
    bugs = bugs.order_by(TblBugTrack.bug_date_receive.desc())
    bugs = bugs.all()
    # for project in projects:
    #     print(project.describe,type(project.describe))
    result = gene_bugtrack_result(self, bugs)
    return result


def get_bugtrack_by_id(self, bug_id):
    bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bug_id).first()
    result = gene_bugtrack_result(self, [bug_track])
    if result:
        return result[0]
    else:
        return []


def gene_bugtrack_result(self, bugs):
    result = []
    for bug in bugs:
        bug_dict = dict()
        bug_dict['bug_id'] = bug.bug_id
        bug_dict['bug_date_receive'] = str(bug.bug_date_receive)
        bug_dict['bug_find_by'] = bug.bug_find_by
        bug_dict['bug_component'] = bug.bug_component
        bug_dict['component_belong'] = bug.component_belong
        bug_dict['component_community'] = bug.component_community
        bug_dict['bug_project_id'] = bug.bug_project_id
        bug_dict['project_version'] = bug.project_version
        bug_dict['bug_describe'] = bug.bug_describe
        bug_dict['bug_level'] = msg_define.BUG_LEVEL[bug.bug_level]
        bug_dict['bug_reason'] = bug.bug_reason
        bug_dict['bug_solution'] = bug.bug_solution
        bug_dict['bug_progress'] = bug.bug_progress
        bug_dict['bug_date_plan'] = str(bug.bug_date_plan)
        bug_dict['bug_date_done'] = str(bug.bug_date_done)
        bug_dict['bug_user_done'] = bug.bug_user_done
        bug_dict['bug_version'] = bug.bug_version
        user = get_user_by_id(self, bug.bug_user_done)
        if user is not None:
            bug_dict['bug_user_done'] = user.username
        user_comp_belong = get_user_by_id(self, bug.component_belong)
        if user_comp_belong is not None:
            bug_dict['component_belong'] = user_comp_belong.username
        user_find_by = get_user_by_id(self, bug.bug_find_by)
        if user_find_by is not None:
            bug_dict['bug_find_by'] = user_find_by.username
        project_name = get_project_by_id(self, bug.bug_project_id)
        if project_name is not None:
            bug_dict['bug_project_id'] = project_name.project_name
        comp_name = get_project_by_id(self, bug.bug_component)
        if comp_name is not None:
            bug_dict['bug_component'] = comp_name.project_name
        result.append(bug_dict)
    return result


class BugTrackHandler(BaseHandler):
    @authenticated
    def get(self):
        belongid = self.get_argument("belongid", None)
        compid = self.get_argument("compid", None)
        blevel = self.get_argument("blevel", None)
        weblog.info("%s.", self._request_summary())
        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid, blevel),
                           users=get_user_list(self), projects=get_project_list(self))
        # return self.render('bug/bugtracklist.html', message="", users=get_user_list(self)
        #                    , projects=get_project_list(self), bugs=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_component = int(self.get_argument("bug_component", '-1'))
        component_belong = int(self.get_argument("component_belong", '-1'))
        bug_level = int(self.get_argument("bug_level", '-1'))
        bug_component = None if bug_component < 0 else bug_component
        component_belong = None if component_belong < 0 else component_belong
        bug_level = None if bug_level < 0 else bug_level
        bugtracks = get_bugtrack_list(self, component_belong, bug_component, bug_level)
        weblog.info("%s. %d %d %d", self._request_summary(), bug_component, component_belong, bug_level)

        return self.write(json.dumps(bugtracks))


class BugTrackAddHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtrackadd.html')
        return self.render('bug/bugtrackadd.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track = TblBugTrack()
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().add(bug_track)
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackEditHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid))
        return self.render('bug/bugtrackedit.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self), bug=get_bugtrack_by_id(self, bid))

    @authenticated
    def post(self, bid):
        weblog.info("%s.", self._request_summary())
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bid).first()
        if bug_track is None:
            msg.append(u"获取问题单为空，问题单id={}".format(bid))
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackedit.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackDeleteHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        bug_track = self.mysqldb().query(TblBugTrack).filter_by(comp_id=bid).first()
        bug_track.bug_project_id = -1
        try:
            self.mysqldb().commit()
        except Exception as e:
            weblog.error("delete bug track id={} error. {}".format(bid, e))
            self.mysqldb().rollback()

        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        # coding=utf-8
import json
from database.tbl_project import TblProject
from database.tbl_bug_list import TblBugList
from database.tbl_account import TblAccount
from database.tbl_bug_track import TblBugTrack
from database.tbl_project_user import TblPorjectUser
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
from tornado.log import access_log as weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord
from handlers.user_manage_handler import get_user_list, get_user_by_id
from handlers.Project.project_manage_handler import get_project_list, get_project_by_id


def get_bugtrack_list(self, belongid=None, compid=None, level=None):
    bugs = self.mysqldb().query(TblBugTrack)
    if belongid is not None:
        bugs = bugs.filter(TblBugTrack.component_belong == belongid)
    if compid is not None:
        bugs = bugs.filter(TblBugTrack.bug_component == compid)
    if level is not None:
        bugs = bugs.filter(TblBugTrack.bug_level == level)
    bugs = bugs.filter(TblBugTrack.bug_project_id > 0)
    bugs = bugs.order_by(TblBugTrack.bug_date_receive.desc())
    bugs = bugs.all()
    # for project in projects:
    #     print(project.describe,type(project.describe))
    result = gene_bugtrack_result(self, bugs)
    return result


def get_bugtrack_by_id(self, bug_id):
    bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bug_id).first()
    result = gene_bugtrack_result(self, [bug_track])
    if result:
        return result[0]
    else:
        return []


def gene_bugtrack_result(self, bugs):
    result = []
    for bug in bugs:
        bug_dict = dict()
        bug_dict['bug_id'] = bug.bug_id
        bug_dict['bug_date_receive'] = str(bug.bug_date_receive)
        bug_dict['bug_find_by'] = bug.bug_find_by
        bug_dict['bug_component'] = bug.bug_component
        bug_dict['component_belong'] = bug.component_belong
        bug_dict['component_community'] = bug.component_community
        bug_dict['bug_project_id'] = bug.bug_project_id
        bug_dict['project_version'] = bug.project_version
        bug_dict['bug_describe'] = bug.bug_describe
        bug_dict['bug_level'] = msg_define.BUG_LEVEL[bug.bug_level]
        bug_dict['bug_reason'] = bug.bug_reason
        bug_dict['bug_solution'] = bug.bug_solution
        bug_dict['bug_progress'] = bug.bug_progress
        bug_dict['bug_date_plan'] = str(bug.bug_date_plan)
        bug_dict['bug_date_done'] = str(bug.bug_date_done)
        bug_dict['bug_user_done'] = bug.bug_user_done
        bug_dict['bug_version'] = bug.bug_version
        user = get_user_by_id(self, bug.bug_user_done)
        if user is not None:
            bug_dict['bug_user_done'] = user.username
        user_comp_belong = get_user_by_id(self, bug.component_belong)
        if user_comp_belong is not None:
            bug_dict['component_belong'] = user_comp_belong.username
        user_find_by = get_user_by_id(self, bug.bug_find_by)
        if user_find_by is not None:
            bug_dict['bug_find_by'] = user_find_by.username
        project_name = get_project_by_id(self, bug.bug_project_id)
        if project_name is not None:
            bug_dict['bug_project_id'] = project_name.project_name
        comp_name = get_project_by_id(self, bug.bug_component)
        if comp_name is not None:
            bug_dict['bug_component'] = comp_name.project_name
        result.append(bug_dict)
    return result


class BugTrackHandler(BaseHandler):
    @authenticated
    def get(self):
        belongid = self.get_argument("belongid", None)
        compid = self.get_argument("compid", None)
        blevel = self.get_argument("blevel", None)
        weblog.info("%s.", self._request_summary())
        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid, blevel),
                           users=get_user_list(self), projects=get_project_list(self))
        # return self.render('bug/bugtracklist.html', message="", users=get_user_list(self)
        #                    , projects=get_project_list(self), bugs=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_component = int(self.get_argument("bug_component", '-1'))
        component_belong = int(self.get_argument("component_belong", '-1'))
        bug_level = int(self.get_argument("bug_level", '-1'))
        bug_component = None if bug_component < 0 else bug_component
        component_belong = None if component_belong < 0 else component_belong
        bug_level = None if bug_level < 0 else bug_level
        bugtracks = get_bugtrack_list(self, component_belong, bug_component, bug_level)
        weblog.info("%s. %d %d %d", self._request_summary(), bug_component, component_belong, bug_level)

        return self.write(json.dumps(bugtracks))


class BugTrackAddHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtrackadd.html')
        return self.render('bug/bugtrackadd.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track = TblBugTrack()
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().add(bug_track)
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackEditHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid))
        return self.render('bug/bugtrackedit.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self), bug=get_bugtrack_by_id(self, bid))

    @authenticated
    def post(self, bid):
        weblog.info("%s.", self._request_summary())
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bid).first()
        if bug_track is None:
            msg.append(u"获取问题单为空，问题单id={}".format(bid))
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackedit.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackDeleteHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        bug_track = self.mysqldb().query(TblBugTrack).filter_by(comp_id=bid).first()
        bug_track.bug_project_id = -1
        try:
            self.mysqldb().commit()
        except Exception as e:
            weblog.error("delete bug track id={} error. {}".format(bid, e))
            self.mysqldb().rollback()

        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        # coding=utf-8
import json
from database.tbl_project import TblProject
from database.tbl_bug_list import TblBugList
from database.tbl_account import TblAccount
from database.tbl_bug_track import TblBugTrack
from database.tbl_project_user import TblPorjectUser
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
from tornado.log import access_log as weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord
from handlers.user_manage_handler import get_user_list, get_user_by_id
from handlers.Project.project_manage_handler import get_project_list, get_project_by_id


def get_bugtrack_list(self, belongid=None, compid=None, level=None):
    bugs = self.mysqldb().query(TblBugTrack)
    if belongid is not None:
        bugs = bugs.filter(TblBugTrack.component_belong == belongid)
    if compid is not None:
        bugs = bugs.filter(TblBugTrack.bug_component == compid)
    if level is not None:
        bugs = bugs.filter(TblBugTrack.bug_level == level)
    bugs = bugs.filter(TblBugTrack.bug_project_id > 0)
    bugs = bugs.order_by(TblBugTrack.bug_date_receive.desc())
    bugs = bugs.all()
    # for project in projects:
    #     print(project.describe,type(project.describe))
    result = gene_bugtrack_result(self, bugs)
    return result


def get_bugtrack_by_id(self, bug_id):
    bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bug_id).first()
    result = gene_bugtrack_result(self, [bug_track])
    if result:
        return result[0]
    else:
        return []


def gene_bugtrack_result(self, bugs):
    result = []
    for bug in bugs:
        bug_dict = dict()
        bug_dict['bug_id'] = bug.bug_id
        bug_dict['bug_date_receive'] = str(bug.bug_date_receive)
        bug_dict['bug_find_by'] = bug.bug_find_by
        bug_dict['bug_component'] = bug.bug_component
        bug_dict['component_belong'] = bug.component_belong
        bug_dict['component_community'] = bug.component_community
        bug_dict['bug_project_id'] = bug.bug_project_id
        bug_dict['project_version'] = bug.project_version
        bug_dict['bug_describe'] = bug.bug_describe
        bug_dict['bug_level'] = msg_define.BUG_LEVEL[bug.bug_level]
        bug_dict['bug_reason'] = bug.bug_reason
        bug_dict['bug_solution'] = bug.bug_solution
        bug_dict['bug_progress'] = bug.bug_progress
        bug_dict['bug_date_plan'] = str(bug.bug_date_plan)
        bug_dict['bug_date_done'] = str(bug.bug_date_done)
        bug_dict['bug_user_done'] = bug.bug_user_done
        bug_dict['bug_version'] = bug.bug_version
        user = get_user_by_id(self, bug.bug_user_done)
        if user is not None:
            bug_dict['bug_user_done'] = user.username
        user_comp_belong = get_user_by_id(self, bug.component_belong)
        if user_comp_belong is not None:
            bug_dict['component_belong'] = user_comp_belong.username
        user_find_by = get_user_by_id(self, bug.bug_find_by)
        if user_find_by is not None:
            bug_dict['bug_find_by'] = user_find_by.username
        project_name = get_project_by_id(self, bug.bug_project_id)
        if project_name is not None:
            bug_dict['bug_project_id'] = project_name.project_name
        comp_name = get_project_by_id(self, bug.bug_component)
        if comp_name is not None:
            bug_dict['bug_component'] = comp_name.project_name
        result.append(bug_dict)
    return result


class BugTrackHandler(BaseHandler):
    @authenticated
    def get(self):
        belongid = self.get_argument("belongid", None)
        compid = self.get_argument("compid", None)
        blevel = self.get_argument("blevel", None)
        weblog.info("%s.", self._request_summary())
        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid, blevel),
                           users=get_user_list(self), projects=get_project_list(self))
        # return self.render('bug/bugtracklist.html', message="", users=get_user_list(self)
        #                    , projects=get_project_list(self), bugs=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_component = int(self.get_argument("bug_component", '-1'))
        component_belong = int(self.get_argument("component_belong", '-1'))
        bug_level = int(self.get_argument("bug_level", '-1'))
        bug_component = None if bug_component < 0 else bug_component
        component_belong = None if component_belong < 0 else component_belong
        bug_level = None if bug_level < 0 else bug_level
        bugtracks = get_bugtrack_list(self, component_belong, bug_component, bug_level)
        weblog.info("%s. %d %d %d", self._request_summary(), bug_component, component_belong, bug_level)

        return self.write(json.dumps(bugtracks))


class BugTrackAddHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtrackadd.html')
        return self.render('bug/bugtrackadd.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track = TblBugTrack()
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().add(bug_track)
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackEditHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid))
        return self.render('bug/bugtrackedit.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self), bug=get_bugtrack_by_id(self, bid))

    @authenticated
    def post(self, bid):
        weblog.info("%s.", self._request_summary())
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bid).first()
        if bug_track is None:
            msg.append(u"获取问题单为空，问题单id={}".format(bid))
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackedit.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackDeleteHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        bug_track = self.mysqldb().query(TblBugTrack).filter_by(comp_id=bid).first()
        bug_track.bug_project_id = -1
        try:
            self.mysqldb().commit()
        except Exception as e:
            weblog.error("delete bug track id={} error. {}".format(bid, e))
            self.mysqldb().rollback()

        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        # coding=utf-8
import json
from database.tbl_project import TblProject
from database.tbl_bug_list import TblBugList
from database.tbl_account import TblAccount
from database.tbl_bug_track import TblBugTrack
from database.tbl_project_user import TblPorjectUser
from handlers.base_handler import BaseHandler
from tornado.web import authenticated
from tornado.log import access_log as weblog
from message import msg_define
from handlers.Email.email_smtp_handler import check_email, check_passord
from handlers.user_manage_handler import get_user_list, get_user_by_id
from handlers.Project.project_manage_handler import get_project_list, get_project_by_id


def get_bugtrack_list(self, belongid=None, compid=None, level=None):
    bugs = self.mysqldb().query(TblBugTrack)
    if belongid is not None:
        bugs = bugs.filter(TblBugTrack.component_belong == belongid)
    if compid is not None:
        bugs = bugs.filter(TblBugTrack.bug_component == compid)
    if level is not None:
        bugs = bugs.filter(TblBugTrack.bug_level == level)
    bugs = bugs.filter(TblBugTrack.bug_project_id > 0)
    bugs = bugs.order_by(TblBugTrack.bug_date_receive.desc())
    bugs = bugs.all()
    # for project in projects:
    #     print(project.describe,type(project.describe))
    result = gene_bugtrack_result(self, bugs)
    return result


def get_bugtrack_by_id(self, bug_id):
    bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bug_id).first()
    result = gene_bugtrack_result(self, [bug_track])
    if result:
        return result[0]
    else:
        return []


def gene_bugtrack_result(self, bugs):
    result = []
    for bug in bugs:
        bug_dict = dict()
        bug_dict['bug_id'] = bug.bug_id
        bug_dict['bug_date_receive'] = str(bug.bug_date_receive)
        bug_dict['bug_find_by'] = bug.bug_find_by
        bug_dict['bug_component'] = bug.bug_component
        bug_dict['component_belong'] = bug.component_belong
        bug_dict['component_community'] = bug.component_community
        bug_dict['bug_project_id'] = bug.bug_project_id
        bug_dict['project_version'] = bug.project_version
        bug_dict['bug_describe'] = bug.bug_describe
        bug_dict['bug_level'] = msg_define.BUG_LEVEL[bug.bug_level]
        bug_dict['bug_reason'] = bug.bug_reason
        bug_dict['bug_solution'] = bug.bug_solution
        bug_dict['bug_progress'] = bug.bug_progress
        bug_dict['bug_date_plan'] = str(bug.bug_date_plan)
        bug_dict['bug_date_done'] = str(bug.bug_date_done)
        bug_dict['bug_user_done'] = bug.bug_user_done
        bug_dict['bug_version'] = bug.bug_version
        user = get_user_by_id(self, bug.bug_user_done)
        if user is not None:
            bug_dict['bug_user_done'] = user.username
        user_comp_belong = get_user_by_id(self, bug.component_belong)
        if user_comp_belong is not None:
            bug_dict['component_belong'] = user_comp_belong.username
        user_find_by = get_user_by_id(self, bug.bug_find_by)
        if user_find_by is not None:
            bug_dict['bug_find_by'] = user_find_by.username
        project_name = get_project_by_id(self, bug.bug_project_id)
        if project_name is not None:
            bug_dict['bug_project_id'] = project_name.project_name
        comp_name = get_project_by_id(self, bug.bug_component)
        if comp_name is not None:
            bug_dict['bug_component'] = comp_name.project_name
        result.append(bug_dict)
    return result


class BugTrackHandler(BaseHandler):
    @authenticated
    def get(self):
        belongid = self.get_argument("belongid", None)
        compid = self.get_argument("compid", None)
        blevel = self.get_argument("blevel", None)
        weblog.info("%s.", self._request_summary())
        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid, blevel),
                           users=get_user_list(self), projects=get_project_list(self))
        # return self.render('bug/bugtracklist.html', message="", users=get_user_list(self)
        #                    , projects=get_project_list(self), bugs=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_component = int(self.get_argument("bug_component", '-1'))
        component_belong = int(self.get_argument("component_belong", '-1'))
        bug_level = int(self.get_argument("bug_level", '-1'))
        bug_component = None if bug_component < 0 else bug_component
        component_belong = None if component_belong < 0 else component_belong
        bug_level = None if bug_level < 0 else bug_level
        bugtracks = get_bugtrack_list(self, component_belong, bug_component, bug_level)
        weblog.info("%s. %d %d %d", self._request_summary(), bug_component, component_belong, bug_level)

        return self.write(json.dumps(bugtracks))


class BugTrackAddHandler(BaseHandler):
    @authenticated
    def get(self):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtrackadd.html')
        return self.render('bug/bugtrackadd.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track = TblBugTrack()
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().add(bug_track)
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackEditHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        # return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self, belongid, compid))
        return self.render('bug/bugtrackedit.html', message="", users=get_user_list(self)
                           , projects=get_project_list(self), bug=get_bugtrack_by_id(self, bid))

    @authenticated
    def post(self, bid):
        weblog.info("%s.", self._request_summary())
        weblog.info("%s.", self._request_summary())
        bug_date_receive = self.get_argument("bug_date_receive", None)
        bug_find_by = int(self.get_argument("bug_find_by", 0))
        bug_component = int(self.get_argument("bug_component", 0))
        component_belong = int(self.get_argument("component_belong", 0))
        component_community = self.get_argument("component_community", None)
        bug_project_id = int(self.get_argument("bug_project_id", 0))
        # project_name = Column(String(1024), nullable=False, comment=u"项目名称")
        project_version = self.get_argument("project_version", None)
        bug_describe = self.get_argument("bug_describe", None)
        bug_level = int(self.get_argument("bug_level", 0))
        bug_reason = self.get_argument("bug_reason", None)
        bug_solution = self.get_argument("bug_solution", None)
        bug_progress = self.get_argument("bug_progress", None)
        bug_date_plan = self.get_argument("bug_date_plan", None)
        bug_date_done = self.get_argument("bug_date_done", None)
        bug_user_done = int(self.get_argument("bug_user_done", 0))
        bug_version = self.get_argument("bug_version", None)
        msg = []
        if bug_date_receive is None:
            msg.append(u"接收日期不能为空")
        if project_version is None:
            msg.append(u"模块所属版本不能为空")
        if bug_date_plan is None or bug_date_done is None:
            msg.append(u"计划日期或解决日期不能为空")
        if bug_version is None:
            msg.append(u"合入版本不能为空")
        bug_track = self.mysqldb().query(TblBugTrack).filter(TblBugTrack.bug_id == bid).first()
        if bug_track is None:
            msg.append(u"获取问题单为空，问题单id={}".format(bid))
        if msg:
            return self.render('bug/bugtrackadd.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))
        bug_track.bug_date_receive = bug_date_receive
        bug_track.bug_find_by = bug_find_by
        bug_track.bug_component = bug_component
        bug_track.component_belong = component_belong
        bug_track.component_community = component_community
        bug_track.bug_project_id = bug_project_id
        bug_track.project_version = project_version
        bug_track.bug_describe = bug_describe
        bug_track.bug_level = bug_level
        bug_track.bug_reason = bug_reason
        bug_track.bug_solution = bug_solution
        bug_track.bug_progress = bug_progress
        bug_track.bug_date_plan = bug_date_plan
        bug_track.bug_date_done = bug_date_done
        bug_track.bug_user_done = bug_user_done
        bug_track.bug_version = bug_version

        try:
            self.mysqldb().commit()
            return self.redirect("/bugtrack/list")
        except Exception as e:
            msg.append(e)
            return self.render('bug/bugtrackedit.html', message=msg, users=get_user_list(self),
                               projects=get_project_list(self))


class BugTrackDeleteHandler(BaseHandler):
    @authenticated
    def get(self, bid):
        weblog.info("%s.", self._request_summary())
        bug_track = self.mysqldb().query(TblBugTrack).filter_by(comp_id=bid).first()
        bug_track.bug_project_id = -1
        try:
            self.mysqldb().commit()
        except Exception as e:
            weblog.error("delete bug track id={} error. {}".format(bid, e))
            self.mysqldb().rollback()

        return self.render('bug/bugtracklist.html', bugtracks=get_bugtrack_list(self))

    @authenticated
    def post(self):
        weblog.info("%s.", self._request_summary())
"""
