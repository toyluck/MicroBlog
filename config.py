import os

basedir = os.path.abspath(os.path.dirname(__file__))
# app.db  address url
SQLALCHEMY_DATABASE_URL = "sqlite:///" + os.path.join(basedir, "app.db")
#  repository position
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, "db_repository")

# cross-site-request-forgery  保持开启状态，可以得到更多的安全
WTF_CSRF_ENABLED = True
SECRET_KEY = "you-never-guess"
OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]
