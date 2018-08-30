import json
from handlers.base_handler import BaseHandler
from exchangelib import DELEGATE, Account, Credentials, Message, Mailbox, HTMLBody, Configuration, FileAttachment
import re
from handlers.Email.email_smtp_handler import generate_code

mail_subject = '注册'
mail_msg_verf = '<p>注册码: {0} </p>'
mail_msg_ca = '<p>文件已发送邮箱. </p>'

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

def Email(self,to, subject, body,email_type, attachments=None):
    creds = Credentials(username=self.localVariable["__EMAILEX__"],
                        password=self.localVariable["__EMAILEX_PASSWORD__"])
    config = Configuration(server='outlook.office365.com',credentials=creds)
    account = Account(
        primary_smtp_address=self.localVariable["__EMAILEX__"],
        config=config,
        # credentials=creds,
        autodiscover=False,
        access_type=DELEGATE
    )
    m = Message(
        account=account,
        subject=subject,
        body=HTMLBody(body),
        to_recipients = [Mailbox(email_address=to)]
    )
    if attachments:
        m.attach(attachments)
    if email_type==1 and to in list(self.localStore.keys()):
        print("清除 %s" % to)
        self.localStore.pop(to)
    try:
        m.send()
        if email_type == 0:
            message = u"验证码已发送邮箱!"
        else:
            message = u"证书已发送邮箱!"
        return message
    except:
        message = u"发送失败!"
        return message

class SendEmailHandler(BaseHandler):

    def get(self):
       self.render("admin/sendemail.html")

    def post(self):
        codeEmailPwd = generate_code(self)
        email_addresss = self.get_argument("email")
        if check_email(email_addresss) is  None:
            return self.write(json.dumps({"msg": u"邮箱不可用!"}))
        receivers = []
        self.localStore[email_addresss] = codeEmailPwd
        receivers.append(email_addresss)
        message = Email(self,receivers[0], mail_subject, mail_msg_verf.format(codeEmailPwd),0)
        print(message)
        return self.write(json.dumps({"msg": message}))

class SendEmailAddressHandler(BaseHandler):

    def get(self):
       self.render("admin/sendemail.html")

    def post(self):

        email_addresss = self.get_argument("email")
        emial_code = self.get_argument("code")
        code_local = None
        email_local = self.localStore.get(email_addresss)
        if email_addresss in list(self.localStore.keys()):
            print(self.localStore)
            code_local = self.localStore.get(email_addresss)
        else:
            return self.write(json.dumps({"msg": u"验证码过期，请重新获取!"}))

        print("local:", code_local, "ui:", emial_code, "localemail:", email_local)
        if code_local is None:
            return self.write(json.dumps({"msg": u"验证码过期!"}))
        # print(codeEmailPwd.get("emailCode"))
        if code_local.upper() != emial_code.upper():
            return self.write(json.dumps({"msg":u"验证码过期!"}))
        receivers = []
        receivers.append(email_addresss)
        try:
            filename = "FileAttachment.txt"
            with open(filename, 'rb') as f:
                my_files = FileAttachment(name=filename, content=f.read())
            message = Email(self,receivers[0], mail_subject, mail_msg_ca, 1, my_files)
            return self.write(json.dumps({"msg": message}))
        except Exception as e:
            print(e)
            return self.write(json.dumps({"msg": u"验证码生成失败!"}))



