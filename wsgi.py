from blog.app import app
from blog.extension import db

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        debug=True,
    )

@app.cli.command("create-users")

def create_users():

    """

    Run in your terminal:

    flask create-users

    > done! created users: <User #1 'admin'> <User #2 'james'>

    """

    from blog.models import User

    admin = User(username="admin", is_staff=True)

    james = User(username="james")

    db.session.add(admin)

    db.session.add(james)

    db.session.commit()

    print("done! created users:", admin, james)