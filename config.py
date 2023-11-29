# 然后使用sqlachemy(app)创建一个db对象
# sqlalchemy 会自动读取app.config中连接数据库的信息
# mysql 所在主机名

HOSTNAME = "127.0.0.1"

PORT = 3306

USERNAME = "root"

PASSWORD = "rootroot"

DATABASE = "zhiliao"

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/dbname'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

# 邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "1084091973@qq.com"
MAIL_PASSWORD = "tnwqautpsiccfiha"
MAIL_DEFAULT_SENDER = "1084091973@qq.com"

SECRET_KEY = "ADJKFLJADLFJDSKLFJ"

#google 配置
GOOGLE_CLIENT_ID = "461968097156-40ledj9drl0t0lqg2khdte3uf4im065q.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
GOOGLE_TOKEN_URL ='https://oauth2.googleapis.com/token'
GOOGLE_ACCESS_TOKEN_PARAMS=None
GOOGLE_AUTHORIZE_URL ='https://accounts.google.com/o/oauth2/auth'
GOOGLE_AUTHORIZE_PARAMS=None,
GOOGLE_API_BASE_URL ='https://www.googleapis.com/oauth2/v1/'
GOOGLE_KWARGS ={'scope': 'openid email profile'}

