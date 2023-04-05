from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound


user = Blueprint("user", __name__, url_prefix="/users", static_folder="../static")

key = [i for i in range(10)]
value = [f'user_{i}' for i in range(10)]

USERS = {key: value for key, value in zip(key, value)}


@user.route("/")
def user_list():
    return render_template(
        "./users/list.html",
        users=USERS,
    )


@user.route("/<int:pk>")
def get_user(pk: int):
    try:
        user_name = USERS[pk]
    except KeyError:
        raise NotFound(f'User ID {pk} is not found')
    return render_template(
        "./users/details.html",
        user_name=user_name,
    )
