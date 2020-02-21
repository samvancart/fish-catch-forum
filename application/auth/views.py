from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user

from application import app, db
from application.auth.models import User
from application.auth.models import Group
from application.auth.forms import LoginForm
from application.auth.forms import SignupForm


@app.route("/auth/login", methods=["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form=LoginForm())

    form = LoginForm(request.form)
    # mahdolliset validoinnit

    user = User.query.filter_by(
        username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", form=form,
                               error="No such username or password")

    login_user(user)
    return redirect(url_for("index"))


@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/auth/signup", methods=["GET", "POST"])
def auth_signup():
    if request.method == "GET":
        return render_template("auth/signupform.html", form=SignupForm())

    form = SignupForm(request.form)
    # mahdolliset validoinnit

    if not form.validate():
        return render_template("auth/signupform.html", form=form,
                               error="Username must be at least 3 characters long")

    user = User.query.filter_by(username=form.username.data).first()
    if user:
        return render_template("auth/signupform.html", form=form,
                               error="Username already taken")

    user = User(username=form.username.data, password=form.password.data)

    group = Group.query.get_or_404(1)

    db.session().add(user)
    group.accounts.append(user)
    db.session().commit()

    login_user(user)
    return redirect(url_for("index"))
