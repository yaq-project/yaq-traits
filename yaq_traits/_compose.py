__all__ = ["compose"]


import collections.abc
import copy
from io import BytesIO

import toml
from fastavro import parse_schema, schemaless_reader, schemaless_writer  # type: ignore
from .__traits__ import traits


def update_recursive(d, u, origin=None):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            if k in ("config", "state", "messages", "properties"):
                d[k] = update_recursive(d.get(k, {}), v, origin)
            else:
                d[k] = update_recursive(d.get(k, {}), v)
                if origin:
                    d[k]["origin"] = origin
        elif k == "types" and isinstance(v, list):
            for ty in v:
                for field in ty.get("fields", []):
                    if field.get("default") == "__null__":
                        field["default"] = None
            d[k] = d.get("types", []) + v
        else:
            d[k] = v
    return d


def merge(o, d, traits=[], origin=None):
    o["traits"] = sorted(set(o["traits"] + traits))
    update_recursive(o, d, origin)
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
        out = merge(out, d, traits=todo, origin=trait)
    # add daemon
    out = merge(out, daemon)
    del out["trait"]
    yaq_defined_types = [
        {
            "type": "record",
            "name": "ndarray",
            "fields": [
                {"name": "shape", "type": {"type": "array", "items": "int"}},
                {"name": "typestr", "type": "string"},
                {"name": "data", "type": "bytes"},
                {"name": "version", "type": "int"},
            ],
            "logicalType": "ndarray",
        },
    ]
    out["types"] = out.get("types", []) + yaq_defined_types
    named_types = {ty["name"]: ty for ty in out["types"]}
    for ty in out["types"]:
        parse_schema(ty, named_schemas=named_types)
    # use fastavro parse_schema to "validate"
    for conf in out.get("config", {}).values():
        if conf.get("default") == "__null__":
            conf["default"] = None
        try:
            parse_schema(conf["type"], named_schemas=named_types)
        except:
            parse_schema(conf, named_schemas=named_types)
    for state in out.get("state", {}).values():
        # Replace TOML null stand-in
        if state.get("default") == "__null__":
            state["default"] = None
        try:
            parse_schema(state["type"], named_schemas=named_types)
        except:
            parse_schema(state, named_schemas=named_types)
    for message in out.get("messages", {}).values():
        if "response" in message.keys():
            parse_schema(
                message["response"], named_schemas=named_types
            )  # will raise exception if invalid
        else:
            message["response"] = "null"
        if "request" in message.keys():
            for msg in message["request"]:
                # Replace TOML null stand-in
                if isinstance(msg, dict) and msg.get("default") == "__null__":
                    msg["default"] = None
                try:
                    parse_schema(msg, named_schemas=named_types)
                except:
                    parse_schema(msg["type"], named_schemas=named_types)
        else:
            message["request"] = []
    for prop in out.get("properties", {}).keys():
        # Run through fastavro to ensure defaults set
        schema = {
            "type": "record",
            "name": "yaq_property",
            "fields": [
                {"name": "getter", "type": "string"},
                {"name": "setter", "type": ["null", "string"], "default": None},
                {"name": "options_getter", "type": ["null", "string"], "default": None},
                {"name": "units_getter", "type": ["null", "string"], "default": None},
                {"name": "limits_getter", "type": ["null", "string"], "default": None},
                {"name": "dynamic", "type": "boolean", "default": True},
                {
                    "name": "control_kind",
                    "type": {
                        "type": "enum",
                        "name": "control_kind",
                        "symbols": ["hinted", "normal", "omitted"],
                    },
                },
                {
                    "name": "record_kind",
                    "type": {
                        "type": "enum",
                        "name": "record_kind",
                        "symbols": ["data", "metadata", "omitted"],
                    },
                },
                {"name": "type", "type": "string"},
            ],
        }

        s = BytesIO()
        schemaless_writer(s, schema, out["properties"][prop])
        s.seek(0)
        out["properties"][prop] = schemaless_reader(s, schema)

    return out


def compose_trait(trait):
    out = copy.deepcopy(traits[trait])
    # add traits
    todo = out.get("requires", [])
    while todo:
        tra = todo.pop(0)
        d = traits[tra]
        todo += d["requires"]
        out = update_recursive(out, d, origin=tra)
    out["trait"] = traits[trait]["trait"]
    out["doc"] = traits[trait]["doc"]
    out["requires"] = traits[trait]["requires"]
    return out
