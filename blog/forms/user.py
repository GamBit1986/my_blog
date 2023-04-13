from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, SubmitField


class UserRegisterForm(FlaskForm):
    username = StringField("Username", [validators.DataRequired()])
    name = StringField("Name")
    email = StringField("E-mail", [validators.DataRequired(), validators.Email()])
    password = PasswordField(
        "Password", [validators.DataRequired(), validators.EqualTo("confirm_password")]
    )
    confirm_password = PasswordField("Confirm Password", [validators.DataRequired()])
    submit = SubmitField("Register")


class UserLoginForm(FlaskForm):
    email = StringField("E-mail", [validators.DataRequired(), validators.Email()])
    password = PasswordField("Password", [validators.DataRequired()])
    submit = SubmitField("Login")
