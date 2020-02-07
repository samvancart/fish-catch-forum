from flask import Flask, redirect, render_template, request, url_for, abort, flash, send_file
from flask_login import login_required, current_user

import os
from application import app, db
from application.group.forms import NewGroup
from application.fish.models import Fish
from application.fish.forms import FishForm
from application.auth.models import User
from application.auth.models import Group
from application.auth.models import groups


@app.route("/groups", methods=["GET"])
def group_index():


    return render_template("group/list.html", groups=Group.query.all(),users=User.query.all())


@app.route("/groups/new", methods=['GET', 'POST'])
@login_required
def group_new():
    form = NewGroup()
    if request.method == 'GET':
        return render_template("group/new.html", form=form,
                title='New group', legend='New group', value='Create group')

    if not form.validate_on_submit():
        return render_template('group/new.html', form=form)
    user = current_user
    g = Group(form.name.data)

    db.session.add(g)
    user.groups.append(g)
    db.session.commit()

    return redirect(url_for("group_index"))