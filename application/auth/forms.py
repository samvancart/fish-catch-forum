from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")

class SignupForm(FlaskForm):
    username = StringField("Username",[validators.DataRequired(message="username cannot be empty"), validators.Length(min=3, max=30, message="Username must be between 3 to 30 characters")])
    password = PasswordField("Password" , [validators.DataRequired(message="password cannot be empty"), validators.Length(min=1, max=30, message="Password must be between 1 to 30 characters")])

    class Meta:
        csrf = False




  