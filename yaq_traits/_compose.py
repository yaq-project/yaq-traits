__all__ = ["compose"]


import pkg_resources
import toml
from fastavro import parse_schema


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
    traits = daemon.pop("traits")
    merge(out, {}, traits=traits)
    while traits:
        trait = traits.pop(0)
        s = pkg_resources.resource_string("yaq_traits", f"../traits/{trait}.toml")
        d = toml.loads(s.decode())
        traits += d["requires"]
        out = merge(out, d, traits=traits)
    # add daemon
    out = merge(out, daemon)
    # use fastavro parse_schema to "validate"
    for message in out["messages"].values():
        if "response" in message.keys():
            parse_schema(message["response"])
        for request in message.get("request", list()):
            parse_schema(request)
    # finish
    return out
