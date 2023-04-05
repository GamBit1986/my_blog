from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound
from flask_login import login_required


user = Blueprint("user", __name__, static_folder="../static")


@user.route("/")
def user_list():

    from ..models import User

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
