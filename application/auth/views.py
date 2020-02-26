from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user

from application import app, db
from application.auth.models import User,groups
from application.group.models import Group
from application.fish.models import Fish
from application.auth.forms import LoginForm
from application.auth.forms import SignupForm
from application.auth.forms import UpdateForm
from application.fish.views import delete_picture



@app.route("/auth/login", methods=["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form=LoginForm())

    form = LoginForm(request.form)
    # mahdolliset validoinnit

    user = User.query.filter_by(
        username=form.username.data, password=form.password.data).first()
    if not user:
        form.username.data=""
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
        form.username.data=""
        return render_template("auth/signupform.html", form=form)

    user = User.query.filter_by(username=form.username.data).first()
    if user:
        form.username.data=""
        return render_template("auth/signupform.html", form=form,
                               error="Username already taken")

    user = User(username=form.username.data, password=form.password.data)

    group = Group.query.get_or_404(1)

    db.session().add(user)
    group.accounts.append(user)
    db.session().commit()

    login_user(user)
    return redirect(url_for("index"))

@app.route("/auth/profile",methods=["GET"])
@login_required
def auth_profile():
    if request.method == "GET":
        return render_template("auth/profile.html")


@app.route("/auth/profile/update",methods=["GET","POST"])
@login_required
def auth_update():
    if request.method == "GET":
        return render_template("auth/update.html", form=UpdateForm())

    form = UpdateForm(request.form)

    if not form.validate():
        return render_template("auth/update.html", form=form)

    user = current_user
    user.password = form.newPassword.data
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/auth/profile/delete",methods=["POST"])
@login_required
def auth_delete():

    user = current_user
    fish = Fish.query.all()

    for f in fish:
        if f.account_id == current_user.id:
            delete_picture(f.image_file)
            db.session.delete(f)

    db.session.delete(user)
    db.session.commit()


    return redirect(url_for("index"))
