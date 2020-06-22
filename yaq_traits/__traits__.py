__all__ = ["traits"]


import os
import pathlib
import toml


here = pathlib.Path(__file__).resolve().parent


traits = {}
for f in os.listdir(here):
    if f.endswith(".toml"):
        name = f.split(".")[0]
        traits[name] = toml.load(here / f)
