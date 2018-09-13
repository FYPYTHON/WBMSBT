python -m pip install pymysqldb
# 项目相关库
    参考requirements.txt
# python 连接SQLalchemy
1）连接参考database/db_config.py.
   需要安装pymysql.
   下载mysql-5.7 ,下载地址：https://dev.mysql.com/downloads/mysql/
   将mysql bin目录加入系统path
   初始化mysql
   .\mysqld --initialize-insecure --user=mysql
   .\mysqld -install
   net start mysql
   修改mysql密码
   alter user 'root'@'localhost' identified by 'Faye0808';
   flush privileges;

2) 忽略警告
    import warnings
    warnings.filterwarnings("ignore")

3) 使用wtform 
   (https://wtforms.readthedocs.io/en/stable/fields.html)
   a.wtform正则表达式：validators.regexp(u'^[^/\\]\.jpg$')
     validators.Regexp(regex, flags=0, message=None)
     flags:eg,re.IGNORECASE
   b.与其他比较，EqualTo
     class ChangePassword(Form):
    	password = PasswordField('New Password', [InputRequired(), EqualTo('confirm', message='Passwords must match')])
    	confirm  = PasswordField('Repeat Password')
   c.长度
     Length(min=-1, max=-1, message=None)
     NumberRange(min=None, max=None, message=None)
#测试

