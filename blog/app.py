from flask import Flask


from blog.user.views import user
from blog.articles.views import articles
from blog.auth.views import auth
from .models import User
from .extension import db, login_manager



def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "4q-z85(2n1r=i+lp7-n%q40abiib(+_5f=3ilwnulq_2^+mqgi"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
    app.config["DEBUG"] = True

    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    db.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


def register_blueprints(app: Flask):
    app.register_blueprint(user)
    app.register_blueprint(articles)
    app.register_blueprint(auth)
