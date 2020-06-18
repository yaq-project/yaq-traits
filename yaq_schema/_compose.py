__all__ = ["compose"]


import pkg_resources
import toml
from fastavro import parse_schema


def compose(daemon):
    out = {}
    traits = daemon["traits"]
    while traits:
        print(traits)
        trait = traits.pop(0)
        s = pkg_resources.resource_string("yaq_schema", f"../traits/{trait}.toml")
        d = toml.loads(s.decode())
        traits += d["requires"]
        for k in ["config", "state", "messages"]:
            if k in out.keys():
                out[k].update(d.pop(k, {}))
        out.update(d)
    out.update(daemon)
    print(type(out))
    parse_schema(out)
    return out
