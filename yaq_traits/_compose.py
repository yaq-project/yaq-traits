__all__ = ["compose"]


import collections.abc

import toml
from fastavro import parse_schema  # type: ignore
from .__traits__ import traits


def update_recursive(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update_recursive(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def merge(o, d, traits=[]):
    o["traits"] = list(set(o["traits"] + traits))
    update_recursive(o, d)
    return o


def compose(daemon):
    out = {}
    out["traits"] = []
    # add traits
    todo = daemon.pop("traits")
    merge(out, {}, traits=todo)
    while todo:
        trait = todo.pop(0)
        d = traits[trait]
        todo += d["requires"]
        out = merge(out, d, traits=todo)
    # add daemon
    out = merge(out, daemon)
    # use fastavro parse_schema to "validate"
    for conf in out.get("config", {}).values():
        if conf.get("default") == "__null__":
            conf["default"] = None
        try:
            parse_schema(conf["type"])
        except:
            parse_schema(conf)
    for state in out.get("state", {}).values():
        # Replace TOML null stand-in
        if state.get("default") == "__null__":
            state["default"] = None
        try:
            parse_schema(state["type"])
        except:
            parse_schema(state)
    for message in out.get("messages", {}).values():
        if "response" in message.keys():
            parse_schema(message["response"])  # will raise exception if invalid
        else:
            message["response"] = "null"
        if "request" in message.keys():
            for msg in message["request"]:
                # Replace TOML null stand-in
                if isinstance(msg, dict) and msg.get("default") == "__null__":
                    msg["default"] = None
                parse_schema(msg)
        else:
            message["request"] = []
    # finish
    return out
