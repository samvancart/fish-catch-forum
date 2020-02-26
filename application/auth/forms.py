from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")

class SignupForm(FlaskForm):
    username = StringField("Username",[validators.DataRequired(), validators.Length(min=3, max=10, message="Username must be between 3 and 10 characters")])
    password = PasswordField("Password",[validators.DataRequired(), validators.Length(min=1, max=10, message="Password must be between 1 and 10 characters")])

    class Meta:
        csrf = False

class UpdateForm(FlaskForm):
    newPassword = PasswordField("New password" , [validators.DataRequired(), validators.Length(min=1, max=10, message="Password must be between 1 and 10 characters")])

    class Meta:
        csrf = False

  