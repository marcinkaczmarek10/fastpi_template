import click

from src.config.db import get_session
from src.api.auth.models import User
from src.api.auth.crypto import get_password_hash


@click.command()
def create_superuser():
    email = click.prompt("Please enter an email", type=str)
    password = click.prompt("Please enter a password", type=str, hide_input=True)
    hashed_password = get_password_hash(password)
    session = get_session()
    with session as session:
        user = User(email=email, password=hashed_password, is_admin=True, is_superuser=True)
        try:
            session.add(user)
            session.commit()
            session.refresh(user)
            click.echo(f"User {email} created!")
        except Exception as err:
            click.echo(err)
