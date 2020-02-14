from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators


class NewGroup(FlaskForm):
    name = StringField("Group name",[validators.Length(min=2,max=20)])

    class Meta:
        csrf = False




  