from flask import g
from flask import request
from flask import session
from flask import url_for
from flask_login import current_user, login_required, logout_user

from app import app, lm, oid, db
from flask import render_template, flash, redirect

from app.models import User
from .forms import LoginForm


@app.route('/')
@app.route("/index")
@login_required
def index():
    user = g.user
    posts = [
        {"author": {'nickname': 'David'}, "job": "do some coolest thing"},
        {"author": {'nickname': "Ivorson"}, 'job': "do worst thing"}
    ]
    return render_template("index.html",
                           user=user,
                           posts=posts
                           )


@app.route("/login", methods=['GET', 'POST'])
@oid.loginhandler
def login():
    # The g global is setup by Flask
    # as a place to store and share data during the life of a request.
    if g.user is not None and g.user.is_authenticated:
        # url_for @link http://flask.pocoo.org/docs/0.11/quickstart/#url-building
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # 拿到 是否记住 保存在 session 中  这个session 是什么？ todo
        session['remember_me'] = form.remember_me.data

        flash("Login request for OpenId =%s,remenber_me=%s" % (
            form.openid.data, str(form.remember_me.data)))
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template("login.html", form=form, title="Sign In",
                           # 要通过[ ‘name’ ]的形式传递
                           providers=app.config['OPENID_PROVIDERS'])


@oid.after_login
def after_openid_login(resp):
    email = resp.email
    print("email = ", email)
    if email is None or email == "":
        flash("Invalid login , Please try again")
        return redirect(url_for('login'))
    user = User.query.filter_by(email=email).first()
    if user is None:
        # store to the db
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = email.split("@")[0]
        user = User(email=email, nickname=nickname)
        db.session.add(user)
        db.session.commit()

    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop("remember_me", None)

    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))


#  before_request will run before the view function each time a request is received
@app.before_request
def before_request():
    g.user = current_user
    db.create_all()


# 这里的装饰 要求 是unicode 的String
@lm.user_loader
def login_user(id):
    return User.query.get(int(id))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
