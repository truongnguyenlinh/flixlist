from app import app, db
from app.models import User
from flask.cli import FlaskGroup


cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    db.session.add(User(email="testing@testing.com"))
    db.session.commit()


if __name__ == "__main__":
    cli()
