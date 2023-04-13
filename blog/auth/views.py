from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import logout_user, login_user, login_required, current_user
from werkzeug.security import check_password_hash

from ..extension import login_manager

from blog.forms.user import UserLoginForm
from ..models import User


auth = Blueprint("auth", __name__, url_prefix="/auth", static_folder="../static")


@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        form = UserLoginForm(request.form)
        errors = []

        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        return render_template(
            "auth/login.html",
            form=form,
            errors=errors,
        )

    if not user or not check_password_hash(user.password, password):
        flash("Check login or password")
        return redirect(url_for(".login"))
    login_user(user)
    return render_template(
        "./users/list.html",
        form=form,
        errors=errors,
    )


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for(".login"))
