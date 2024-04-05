import click

from src.commands.create_superuser import create_superuser


@click.group()
def cli():
    pass


cli.add_command(create_superuser)

if __name__ == "__main__":
    cli()
