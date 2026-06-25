__all__ = ["traits"]


import os
import pathlib
try:
    import tomllib as toml
except ImportError:
    import toml as toml

here = pathlib.Path(__file__).resolve().parent

traits = {}
for f in os.listdir(here):
    if f.endswith(".toml"):
        name = f.split(".")[0]
        traits[name] = toml.load((here / f).open("rb"))
