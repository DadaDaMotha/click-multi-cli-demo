import click
from rich import print


@click.command()
def hello_world():
    print("hello world")
