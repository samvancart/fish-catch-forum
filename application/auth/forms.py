from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")

class SignupForm(FlaskForm):
    username = StringField("Username" ,[validators.Length(min=3,max=20)])
    password = PasswordField("Password",[validators.Length(max=60)])

    class Meta:
        csrf = False




  