from os import getenv, path
from json import load
import os

from werkzeug.security import generate_password_hash
from flask import Flask

from blog.user.views import user
from blog.articles.views import articles
from blog.auth.views import auth
from blog.authors.views import author
from .models import User

from .extension import db, login_manager, migrate, csrf


app = Flask(__name__)


""" def create_app() -> Flask:
    

    return app """


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)

    csrf.init_app(app)


    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


def register_blueprints(app: Flask):
    app.register_blueprint(user)
    app.register_blueprint(articles)
    app.register_blueprint(auth)
    app.register_blueprint(author)


def register_commands(app: Flask):
    # app.cli.add_command(init_db)
    app.cli.add_command(create_users)
    app.cli.add_command(create_admin)



""" @app.cli.command("init-db")
def init_db():
    
    Run in your terminal:
    flask init-db
    
    db.create_all()
    print("done!") """



@app.cli.command("create-users")
def create_users():
    from blog.models import User

    db.session.add(User(email="aaaa@test.com", password=generate_password_hash("test")))
    db.session.add(
        User(email="test2@test.com", password=generate_password_hash("test2"))
    )
    db.session.add(
        User(email="test3@test.com", password=generate_password_hash("test3"))
    )

    db.session.commit()


@app.cli.command("create-admin")
def create_admin():
    """

    Run in your terminal:

    flask create-users


    > done! created users: <User #1 'admin'>

    """

    from blog.models import User

    admin = User(username="admin", is_staff=True)

    db.session.add(admin)

    db.session.commit()

    print("done! created users:", admin)


app.config.from_object("blog.config")

migrate.init_app(app, db, compare_type=True)

register_commands(app)
register_extensions(app)
register_blueprints(app)
