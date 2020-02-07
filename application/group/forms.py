from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators


class NewGroup(FlaskForm):
    name = StringField("Group name")

    class Meta:
        csrf = False




  