from app import app
from flask import render_template, flash, redirect
from .forms import LoginForm


@app.route('/')
@app.route("/index")
def index():
    user = {'nickname': '黄一川'}
    posts = [
        {"author": {'nickname': 'David'}, "job": "do some coolest thing"},
        {"author": {'nickname': "Ivorson"}, 'job': "do worst thing"}
    ]
    return render_template("index.html",
                           user=user,
                           posts=posts
                           )


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("Login request for OpenId =%s,remenber_me=%s" % (
        form.openid.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template("login.html", form=form, title="Sign In",
                           # 要通过[ ‘name’ ]的形式传递
                           providers=app.config['OPENID_PROVIDERS'])
