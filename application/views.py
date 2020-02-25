from flask import render_template
from application import app
from application.auth.models import User

@app.route("/")
def index():
    users_and_posts = User.users_and_posts()
    return render_template("index.html",users_and_posts=users_and_posts)
