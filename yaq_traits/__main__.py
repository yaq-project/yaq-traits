import click
import toml as toml_
import json
import prettytable  # type: ignore
from colorama import Fore  # type: ignore

from .__version__ import __version__
from ._check import check as check_
from ._compose import compose as compose_, compose_trait
from .__traits__ import traits


@click.group()
@click.version_option(__version__)
def main():
    pass


@main.command(name="check")
@click.argument("avpr", nargs=1)
def check(avpr):
    with open(avpr, "r") as f:
        d = json.load(f)
    out = prettytable.PrettyTable()
    out.field_names = ["trait", "expected", "measured"]
    out.align = "l"
    bad = []
    try:
        for k, v in check_(d).items():
            # expected
            if k in d["traits"]:
                expected = Fore.GREEN + "true" + Fore.RESET
            else:
                expected = Fore.RED + "false" + Fore.RESET
            # measured
            if v:
                status = Fore.GREEN + "true" + Fore.RESET
            else:
                status = Fore.RED + "false" + Fore.RESET
            out.add_row([k, expected, status])
            # bad
            if k in d["traits"] and not v or v and k not in d["traits"]:
                bad.append(k)
    except Exception as e:
        raise click.ClickException(e)
    click.echo(out)
    if bad:
        message = "failed to verify expected trait(s):"
        for trait in bad:
            message += f"\n  {trait}"
        raise click.ClickException(message)


@main.command(name="compose")
@click.argument("toml", nargs=1)
def compose(toml):
    d = toml_.load(toml)
    pr = compose_(d)
    check_(pr)
    s = json.dumps(pr, indent=4, sort_keys=True)
    click.echo(s)


@main.command(name="get")
@click.argument("trait", nargs=1)
def get(trait):
    pr = compose_trait(trait)
    s = json.dumps(pr, indent=4, sort_keys=True)
    click.echo(s)


@main.command(name="list")
def list():
    for t in sorted(traits.keys()):
        print(t)
