# coding=utf-8
import json
import random
from tornado.web import authenticated
from handlers.base_handler import BaseHandler
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
import re
import os
from tornado.log import access_log as weblog


def check_email(email):
    pattern = "^[\.a-zA-Z0-9_-]+@[\.a-zA-Z0-9_-]+"
    issue = re.compile(pattern)
    result = issue.match(email)
    return result


def check_passord(pwd):
    pattern = "^(\w){6,20}$"
    issue = re.compile(pattern)
    result = issue.match(pwd)
    return result


def generate_code(self):
    try:
        _letter_cases = "abcdefghjkmnpqrstuvwxy"
        _upper_cases = "ABCDEFGHJKLMNPQRSTUVWXY"
        _numbers = "1234567890"
        init_chars = ''.join((_letter_cases, _upper_cases, _numbers))
        strs = ''.join(random.sample(init_chars, 4))
        self.localStore["code"] = strs
        return strs
    except:
        print("verifyCode is error")
        return None


def sendEmail(self,emailAdd,content,content_type = 0):

    msgRoot = MIMEMultipart('related')
    msgRoot['From'] = self.localVariable["__MAIL__"]
    msgRoot['To'] = "".join(emailAdd)
    subject = '验证码'
    msgRoot['Subject'] = Header(subject, 'utf-8')

    mail_msg = "<p>欢迎注册，您的验证码为： {code}</p>".format(code=content)

    msgRoot.attach(MIMEText(mail_msg, 'html', 'utf-8'))

    mailserver = "smtp.qq.com"            # 账号 qq 邮箱
    port = 465
    try:
        smtpObj = smtplib.SMTP_SSL(mailserver, port)
        # smtpObj = smtplib.SMTP(mailserver, port)
        sender = self.localVariable["__MAIL__"]
        passwd = self.localVariable["__MAIL_PASSWORD__"]
        smtpObj.login(sender, passwd)
        # smtpObj.set_debuglevel(1)
        # smtpObj.docmd("EHLO server")
        # smtpObj.docmd("AUTH LOGIN")
        smtpObj.sendmail(sender, emailAdd, msgRoot.as_string())
        self.write(json.dumps({"code": content}))
        weblog.info("邮件发送成功。", self._request_summary())
    except smtplib.SMTPException as e:
        weblog.info("Error: 无法发送邮件", self._request_summary(), e)


class SendEmailHandler(BaseHandler):
    @authenticated
    def get(self):
       self.render("admin/sendemail.html")

    @authenticated
    def post(self):
        codeEmailPwd = generate_code(self)
        email_addresss = self.get_argument("email")
        if check_email(email_addresss) is  None:
            return self.write(json.dumps({"msg": u"邮箱格式错误!"}))
        receivers = []

        self.localStore[email_addresss] = codeEmailPwd
        receivers.append(email_addresss)
        sendEmail(self,receivers,codeEmailPwd)



