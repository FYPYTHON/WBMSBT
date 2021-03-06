# coding=utf-8
from .extra_url import extra_url
from handlers import admin_handler, home_handler, user_setting_handler, user_manage_handler, note_manage_handler
from handlers import main_handler,table_test_handler
from handlers.signin_handler import SigninHandler
from handlers.Email import email_smtp_handler,email_exchange_handler
from handlers.Chart import chart_manage_handler
from handlers.Project import project_manage_handler
from handlers.Project import task_manage_handler
from handlers.Bug import bug_manage_handler, bug_track_handler, bug_maintenance_handler

url = [                            #
        (r'/', SigninHandler),
        (r'/signin', SigninHandler),
        (r'/logout', SigninHandler),
        (r'/homepage', main_handler.MainHandler),
        (r'/home', main_handler.MainHandler),
        (r'/admin/verifyCode', admin_handler.verifyCode),
        (r'/test', table_test_handler.TableTestHandler),
        (r'/sendEmail/stmp',email_smtp_handler.SendEmailHandler),
        (r'/sendEmail/exchange',email_exchange_handler.SendEmailHandler),
        (r'/home', home_handler.HomeHandler),
        (r'/chart', chart_manage_handler.ChartManageHandler),
        (r'/usersetting', user_setting_handler.UserSettingHandler),
        (r'/user/add', user_manage_handler.UserAddHandler),
        (r'/user/list', user_manage_handler.UserListHandler),
        (r'/user/edit/([0-9]+)', user_manage_handler.UserEditHandler),
        (r'/user/delete/([0-9]+)', user_manage_handler.UserDeleteHandler),
        (r'/note/list', note_manage_handler.NoteListHandler),
        (r'/project/list', project_manage_handler.ProjectListHandler),
        (r'/project/add', project_manage_handler.ProjectAddHandler),
        (r'/project/delete/([0-9]+)', project_manage_handler.ProjectDeleteHandler),
        (r'/task', task_manage_handler.TaskManageHandler),
        # bug manager
        (r'/bug/list', bug_manage_handler.BugListHandler),
        (r'/bug/add', bug_manage_handler.BugAddHandler),
        (r'/bug/edit/([0-9]+)', bug_manage_handler.BugEditHandler),
        (r'/bug/delete/([0-9]+)', bug_manage_handler.BugDeleteHandler),
        # bug track list
        (r'/bugtrack/list', bug_track_handler.BugTrackHandler),
        (r'/bugtrack/add', bug_track_handler.BugTrackAddHandler),
        (r'/bugtrack/edit/([0-9]+)', bug_track_handler.BugTrackEditHandler),
        (r'/bugtrack/delete/([0-9]+)', bug_track_handler.BugTrackDeleteHandler),
        # component maintenance
        (r'/compmt/list', bug_maintenance_handler.BugCompmtListHandler),
        (r'/compmt/add', bug_maintenance_handler.BugCompmtAddHandler),
        (r'/compmt/edit/([0-9]+)', bug_maintenance_handler.BugCompmtEditHandler),
        (r'/compmt/delete/([0-9]+)', bug_maintenance_handler.BugCompmtDeleteHandler),

] + extra_url
