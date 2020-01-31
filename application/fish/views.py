from flask import redirect, render_template, request, url_for
from flask_login import login_required,current_user

from application import app, db
from application.fish.models import Fish
from application.fish.forms import FishForm


@app.route("/fish", methods=["GET"])
def fish_index():
    return render_template("fish/list.html", fish=Fish.query.all())


@app.route("/fish/new/")
@login_required
def fish_form():
    return render_template("fish/new.html", form=FishForm())


@app.route("/fish/", methods=["POST"])
@login_required
def fish_create():
    form = FishForm(request.form)

    if not form.validate():
        return render_template("fish/new.html", form=form)

    f = Fish(form.species.data)
    f.weight = form.weight.data
    f.account_id = current_user.id

    db.session().add(f)
    db.session().commit()

    return redirect(url_for("fish_index"))


@app.route("/fish/delete", methods=["POST"])
@login_required
def fish_delete():

    # species = request.form.get("species")
    # f = Fish.query.filter_by(species=species).first()

    form = FishForm(request.form)
    f = Fish.query.filter_by(species=form.species.data).first()

    db.session.delete(f)
    db.session().commit()

    return redirect(url_for("fish_index"))
