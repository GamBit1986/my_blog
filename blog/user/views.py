from flask import Blueprint, render_template, redirect, url_for, request
from werkzeug.exceptions import NotFound
from werkzeug.security import generate_password_hash
from flask_login import logout_user, login_user, login_required, current_user

from blog.forms.user import UserRegisterForm
from ..models import User
from ..extension import db

user = Blueprint("user_problem", __name__, static_folder="../static")


@user.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("user_problem.get_user", pk=current_user.id))

    form = UserRegisterForm(request.form)
    errors = []
    if request.method == "POST" and form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).count():
            form.email.errors.append("Email isn't unique")
            return render_template(
                "./users/register.html",
                form=form,
                errors=errors,
            )
        _user = User(
            username=form.username.data,
            name=form.name.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data),
            is_staff=False,
        )

        db.session.add(_user)
        db.session.commit()

        login_user(_user)

    return render_template(
        "./users/register.html",
        form=form,
        errors=errors,
    )


@user.route("/")
def user_list():
    users = User.query.all()
    return render_template(
        "./users/list.html",
        users=users,
    )


@user.route("/<int:pk>")
@login_required
def get_user(pk: int):
    from ..models import User

    user = User.query.filter_by(id=pk)
    if user is None:
        raise NotFound(f"User id:{pk}, not found")

    return render_template(
        "./users/profile.html",
        user=user,
    )
