python -m pip install pymysqldb
# 项目相关库
    环境：python3.5
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
   alter user 'root'@'localhost' identified by 'xxxxxxxx';
   flush privileges;

2) 忽略警告
    import warnings
    warnings.filterwarnings("ignore")
    a、Warning: (1287, "'@@tx_isolation' is deprecated and will be removed in a future release. Please use '@@transaction_isolation' instead")
        result = self._query(query)
       将site-packages\sqlalchemy\dialects\mysql\base.py中@@tx_isolation替换为@@transaction_isolation

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
4）常用网站
   图标：bootstrap , 用法：user  --> icon-user
   a、http://glyph.smarticons.co/#usage
   b、http://www.bootstrapicons.com/index.htm?version=3.0.2
   bootstrap:https://v3.bootcss.com/components/#btn-groups
# 添加redis服务
   将redis加到Windows服务中。首先还是要启动redis服务器端，然后在运行redis客户端，
   然后通过Windows的service-install命令，输入：
    redis-server --service-install redis.windows.conf --loglevel verbose  
#测试更新
1、 添加multiple-select.js/css。
2、 增加message序列化和反序列。




