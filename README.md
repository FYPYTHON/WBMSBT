python -m pip install pymysqldb
# ��Ŀ��ؿ�
    ������python3.5
    �ο�requirements.txt
# python ����SQLalchemy
1�����Ӳο�database/db_config.py.
   ��Ҫ��װpymysql.
   ����mysql-5.7 ,���ص�ַ��https://dev.mysql.com/downloads/mysql/
   ��mysql binĿ¼����ϵͳpath
   ��ʼ��mysql
   .\mysqld --initialize-insecure --user=mysql
   .\mysqld -install
   net start mysql
   �޸�mysql����
   alter user 'root'@'localhost' identified by 'xxxxxxxx';
   flush privileges;

2) ���Ծ���
    import warnings
    warnings.filterwarnings("ignore")
    a��Warning: (1287, "'@@tx_isolation' is deprecated and will be removed in a future release. Please use '@@transaction_isolation' instead")
        result = self._query(query)
       ��site-packages\sqlalchemy\dialects\mysql\base.py��@@tx_isolation�滻Ϊ@@transaction_isolation

3) ʹ��wtform 
   (https://wtforms.readthedocs.io/en/stable/fields.html)
   a.wtform������ʽ��validators.regexp(u'^[^/\\]\.jpg$')
     validators.Regexp(regex, flags=0, message=None)
     flags:eg,re.IGNORECASE
   b.�������Ƚϣ�EqualTo
     class ChangePassword(Form):
    	password = PasswordField('New Password', [InputRequired(), EqualTo('confirm', message='Passwords must match')])
    	confirm  = PasswordField('Repeat Password')
   c.����
     Length(min=-1, max=-1, message=None)
     NumberRange(min=None, max=None, message=None)
4��������վ
   ͼ�꣺bootstrap , �÷���user  --> icon-user
   a��http://glyph.smarticons.co/#usage
   b��http://www.bootstrapicons.com/index.htm?version=3.0.2
   bootstrap:https://v3.bootcss.com/components/#btn-groups
# ���redis����
   ��redis�ӵ�Windows�����С����Ȼ���Ҫ����redis�������ˣ�Ȼ��������redis�ͻ��ˣ�
   Ȼ��ͨ��Windows��service-install������룺
    redis-server --service-install redis.windows.conf --loglevel verbose  
#���Ը���
1�� ���multiple-select.js/css��
2�� ����message���л��ͷ����С�
3�� ����session����¼��֤��




