from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.openid import OpenID
from flask_login import LoginManager
from config import basedir
from os import path

app = Flask(__name__)
# 导入config
app.config.from_object("config")
db = SQLAlchemy(app)

# 设置登录 LoginManager
lm = LoginManager()
lm.init_app(app)
# 设置保存openid 的位置
oid = OpenID(app, path.join(basedir, "tmp"))
lm.login_view = 'login'
from app import views, models
