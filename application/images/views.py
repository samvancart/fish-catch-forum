from application import app, db
from flask import redirect, render_template, request, url_for
from application.images.models import Image


@app.route("/images", methods=["GET"])
def images_index():
    return render_template("images/list.html", images=Image.query.all())


@app.route("/images/new/")
def images_form():
    return render_template("images/new.html")


@app.route("/images/", methods=["POST"])
def images_create():
    t = Image(request.form.get("weight"))

    db.session().add(t)
    db.session().commit()

    return redirect(url_for("images_index"))
