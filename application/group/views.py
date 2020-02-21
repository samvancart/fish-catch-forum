from flask import Flask, redirect, render_template, request, url_for, abort, flash, session
from flask_login import login_required, current_user

import os
from application import app, db, set_session_group

from application.group.forms import NewGroup
from application.fish.models import Fish
from application.fish.forms import FishForm
from application.auth.models import User,groups
from application.group.models import Group



@app.route("/groups", methods=["GET"])
def group_index():
    groups=Group.query.all()
    users=User.query.all()
    return render_template("group/list.html", groups=groups, users=users)


@app.route("/groups/new", methods=['GET', 'POST'])
@login_required
def group_new():
    form = NewGroup()

    if request.method == 'GET':
        return render_template("group/new.html", form=form,
                title='New group', legend='New group', value='Create group')

    if not form.validate_on_submit():
        return render_template('group/new.html', form=form,
                title='New group', legend='New group', value='Create group')
    user = current_user
    g = Group(form.name.data)

    db.session.add(g)
    user.groups.append(g)
    db.session.commit()

    return redirect(url_for("group_index"))


@app.route("/groups/<int:group_id>/join")
@login_required
def group_join(group_id):
    group = Group.query.get_or_404(group_id)
    user = current_user
    users=User.query.all()
    groups=Group.query.all()

    group.accounts.append(user)
    db.session.commit()

    for user in group.accounts:
        print("Users in group ",group.name,": ",user.username)

        return redirect(url_for("group_index",group_id=group_id))

@app.route("/groups/<int:group_id>/leave")
@login_required
def group_leave(group_id):
    group = Group.query.get_or_404(group_id)
    user = current_user

    group.accounts.remove(user)
    db.session.commit()

    print("GROUP_LEAVE ACTIVE GROUP: ",group_id)
    
    for user in group.accounts:
        print("Users in group ",group.name,": ",user.username)

    return redirect(url_for("group_index",group_id=group_id))

@app.route("/groups/<int:group_id>")
def group_view(group_id):
    set_session_group(group_id)

    fish = Fish.query.all()

    users= User.query.join(groups).join(Group).filter((groups.c.account_id == User.id)
    & (groups.c.group_id == group_id)).all()
    
    if not len(users) == 0:
       no_posts = User.find_users_with_no_posts(group_id)
    else:
         no_posts = []

    return redirect(url_for("fish_index",group_id=group_id))
