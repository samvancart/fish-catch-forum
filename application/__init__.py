from flask import Flask,g,current_app,session
app = Flask(__name__)


# database connectivity and ORM
from sqlalchemy import event, DDL
from flask_sqlalchemy import SQLAlchemy

import os


if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///fish.db"
    app.config["SQLALCHEMY_ECHO"] = True

# clear cache confif
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB

db = SQLAlchemy(app)


# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

# login
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager,current_user
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality."



# roles in login_required
from functools import wraps

def login_required(_func=None, *, role="ANY"):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not (current_user and current_user.is_authenticated):
                return login_manager.unauthorized()

            acceptable_roles = set(("ANY", *current_user.roles()))

            if role not in acceptable_roles:
                return login_manager.unauthorized()

            return func(*args, **kwargs)
        return decorated_view
    return wrapper if _func is None else wrapper(_func)


@app.before_first_request
def init_session_group():
    group = Group.query.get(1)
    session['group'] = group.id
    print("SESSION_GROUP: ",session['group'])
    inject_group()

def set_session_group(group_id):
    session.pop('group',None)
    session['group'] = group_id
    inject_group()


@app.context_processor
def inject_group():
    id = session['group']
    active_group=Group.query.get(id)
    # active_group=Group.query.get(1)
    print('@app.context_processor: ',active_group.id)
    return dict(active_group=active_group)   


from application.group.models import Group

    

# load application content
from application import views

from application.fish import models
from application.fish import views

from application.auth import models
from application.auth import views

from application.group import views



# login functionality, part 2
from application.auth.models import User






@event.listens_for(Group.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db.session.add(Group(name='Main'))
    db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



try:  
    db.create_all()
except:
    pass