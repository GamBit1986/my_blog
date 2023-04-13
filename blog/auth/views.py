from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import logout_user, login_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from ..extension import login_manager

from blog.forms.user import UserLoginForm
from ..models import User


auth = Blueprint("auth", __name__, url_prefix="/auth", static_folder="../static")


@auth.route("/login", methods=["POST", "GET"])
def login():
    form = UserLoginForm(request.form)
    errors = []

    if request.method == "GET":
        return render_template(
            "auth/login.html",
            form=form,
            errors=errors,
        )
    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).one_or_none()
        if user is None:
            return render_template(
                "auth/login.html", form=form, error="username doesn't exist"
            )
        if not check_password_hash(user.password, form.password.data):
            return render_template(
                "auth/login.html", form=form, error="invalid username or password"
            )

        login_user(user)
        users = User.query.all()
        return render_template("./users/list.html", users=users)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for(".login"))
