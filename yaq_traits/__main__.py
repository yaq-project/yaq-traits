import click
import toml as toml_
import json

from .__version__ import __version__
from ._compose import compose as compose_


@click.group()
@click.version_option(__version__)
def main():
    pass


@main.command(name="check")
def check():
    raise NotImplementedError


@main.command(name="compose")
@click.argument("toml", nargs=1)
def compose(toml):
    d = toml_.load(toml)
    pr = compose_(d)
    s = json.dumps(pr, indent=4, sort_keys=True)
    click.echo(s)
