from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound

from ..user.views import USERS


articles = Blueprint(
    "articles", __name__, url_prefix="/articles", static_folder="../static"
)

ARTICLE = {
    0: {
        "Title": "Title 1",
        "Text": "Lorem ipsum, dolor sit amet consectetur adipisicing elit. Facilis, non ipsum quae saepe a ducimus nemo ratione ipsam totam doloribus debitis! Illo ullam ducimus ab vero numquam autem, excepturi alias!Lorem ipsum dolor sit amet consectetur adipisicing elit. Nostrum, ipsam",
        "User": USERS[3],
    },
    1: {
        "Title": "Title 2",
        "Text": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Nostrum, ipsam?",
        "User": USERS[1],
    },
}


@articles.route("/")
def article_list():
    return render_template(
        "./articles/list.html",
        article=ARTICLE,
    )


@articles.route("/<int:pk>")
def get_article(pk: int):
    try:
        article_dict = ARTICLE[pk]
        users = USERS
    except IndexError:
        raise NotFound(f"User ID {pk} is not found")
    return render_template(
        "./articles/details.html", article_dict=article_dict, users=users
    )
