__all__ = ["compose"]


import toml
from fastavro import parse_schema  # type: ignore
from .__traits__ import traits


def merge(o, d, traits=[]):
    for k in ["config", "state", "messages"]:
        if k in o.keys():
            o[k].update(d.pop(k, {}))
    o["traits"] = list(set(o["traits"] + traits))
    o.update(d)
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
    for message in out.get("messages", {}).values():
        if "response" in message.keys():
            parse_schema(message["response"])  # will raise exception if invalid
        else:
            message["response"] = "null"
        if "request" in message.keys():
            parse_schema(request)
        else:
            message["request"] = []
    # finish
    return out
