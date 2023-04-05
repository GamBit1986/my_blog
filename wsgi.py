
from blog.app import create_app, db
from werkzeug.security import generate_password_hash


app = create_app()


@app.cli.command("init-db")
def init_db():
    db.create_all()


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

