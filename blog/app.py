from os import getenv, path
from json import load
import os

from werkzeug.security import generate_password_hash
from flask import Flask
from flask_combo_jsonapi import Api

from blog.user.views import user
from blog.articles.views import article
from blog.auth.views import auth
from blog.authors.views import author
from .models import User
from blog.admin.routes import admin

from .extension import db, login_manager, migrate, csrf, create_api_spec_plugin, create_event_plugin, create_permission_plugin


app = Flask(__name__)


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    csrf.init_app(app)
    admin.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


def register_blueprints(app: Flask):
    app.register_blueprint(user, name="user_bp")
    app.register_blueprint(article, name="article_bp")
    app.register_blueprint(auth)
    app.register_blueprint(author)


def register_commands(app: Flask):
    app.cli.add_command(create_tags)
    app.cli.add_command(create_admin)


def register_api(app: Flask):
    from blog.api.tag import TagList, TagDetail
    from blog.api.user import UserList, UserDetail
    from blog.api.author import AuthorList, AuthorDetail
    from blog.api.article import ArticleList, ArticleDetail

    api = Api(
        app=app,
        plugins=[
            create_api_spec_plugin(app),
              create_event_plugin(app),
              create_permission_plugin(app),
              ]
    )
    
    
    api.route(TagList, "tag_list", "/api/tags", tag="Tag")
    api.route(TagDetail, "tag_detail", "/api/tags/<int:id>", tag="Tag" )

    api.route(UserList, "user_list", "/api/users", tag="User")
    api.route(UserDetail, "user_detail", "/api/users/<int:id>", tag="User")

    api.route(AuthorList, "author_list", "/api/authors", tag="Author")
    api.route(AuthorDetail, "author_detail", "/api/authors/<int:id>", tag="Author")

    api.route(ArticleList, "article_list", "/api/articles", tag="Article")
    api.route(ArticleDetail, "article_detail", "/api/articles/<int:id>", tag="Article")


@app.cli.command("create-tags")
def create_tags():
    """

    Run in your terminal:

    flask create-tags

    """

    from blog.models import Tag

    for name in [
        "flask",
        "django",
        "python",
        "sqlalchemy",
        "news",
    ]:
        tag = Tag(name=name)
        db.session.add(tag)
    db.session.commit()
    print("created tags")

@app.cli.command("create-admin")
def create_admin():


    """
    Run in your terminal:
    ➜ flask create-admin
    > created admin: <User #1 'admin'>
    """
    from blog.models import User

    admin = User(username="admin", is_staff=True, name="admin", email="admin@mail.ru", password=generate_password_hash("admin"))    
    db.session.add(admin)
    db.session.commit()
    print("created admin:", admin)

app.config.from_object("blog.config")

migrate.init_app(app, db, compare_type=True)

register_commands(app)
register_extensions(app)
register_blueprints(app)
register_api(app)
