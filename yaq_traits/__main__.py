import itertools
import json
import pathlib
import traceback

import click
import toml as toml_
import prettytable  # type: ignore
from colorama import Fore  # type: ignore

from .__version__ import __version__
from ._check import check as check_
from ._compose import compose as compose_, compose_trait
from ._config_schema import main as compose_config
from .__traits__ import traits


@click.group()
@click.version_option(__version__)
def main():
    pass


@main.command(name="check")
@click.option("--fix", is_flag=True, default=False)
@click.argument("avprs", nargs=-1)
def check(avprs, fix=False):
    if not avprs:
        avprs = (".",)
    exit_bad = {}
    avprs_chain = []
    for avpr in avprs:
        avpr = pathlib.Path(avpr)
        if avpr.is_dir():
            avprs_chain.append(avpr.glob("**/*.avpr"))
        else:
            avprs_chain.append([avpr])

    for avpr in itertools.chain(*avprs_chain):
        click.echo(avpr)
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
            exit_bad[avpr] = message
            if fix:
                avpr_path = pathlib.Path(avpr)
                toml_path = avpr_path.with_suffix(".toml")
                if toml_path.exists():
                    with open(avpr_path, "w") as f:
                        d = toml_.load(toml_path)
                        pr = compose_(d)
                        check_(pr)
                        f.write(json.dumps(pr, indent=4, sort_keys=True))

    if exit_bad:
        message = "\n\n".join(f"{k}: {v}" for k, v in exit_bad.items())
        raise click.ClickException(message)


@main.command(name="compose")
@click.option("--save", is_flag=True, default=False)
@click.argument("toml", nargs=-1)
def compose(toml, save):
    """Generate avpr file(s) from tomls.

    Argument TOML takes single path to toml or directory.

    Default directs output to stdout. Flag SAVE directs to file automatically.
    """
    # handle case of empty input
    if not toml:
        tomls = "."
    else:
        tomls = toml
    # process one at a time
    for toml in tomls:
        toml = pathlib.Path(toml)
        if toml.is_file():
            todo = [toml]
        else:
            todo = toml.glob("**/*.toml")
        for toml in todo:
            try:
                d = toml_.load(toml)
                pr = compose_(d)
                check_(pr)
                s = json.dumps(pr, indent=4, sort_keys=True)
            except Exception:
                print(f"Exception while processing {toml}:", traceback.format_exc(0).strip())
                continue
            # now process pr
            schema = compose_config(pr)
            if save:
                outfile1 = toml.with_suffix(".avpr")
                outfile2 = toml.with_name(f"{toml.stem}_config.json")
                outfile1.write_text(s)
                click.echo(f"{toml} > {outfile1}")
                outfile2.write_text(json.dumps(schema, indent=4, sort_keys=True))
                click.echo(f"{toml} > {outfile2}")
            else:
                click.echo(s)
                click.echo()


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
