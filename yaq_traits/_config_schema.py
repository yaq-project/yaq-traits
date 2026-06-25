"""create config schema validation"""

import json
from fastavro import parse_schema
import subprocess


def main(avpr):
    config = avpr["config"]

    # step 1: make a valid avro protocol for the config
    named_types = {ty["name"]: ty for ty in avpr.get("types", [])}
    named_schemas = {}
    for ty in named_types.values():
        parse_schema(ty, named_schemas=named_schemas)
    # warning: does not handle arbitrary nested types atm
    for ty in named_types.values():
        # make record field types explicit
        if ty.get("type", "") == "record":
            for fi in ty["fields"]:
                if (type_ := fi["type"]) in [_ for _ in named_types.keys()]:
                    fi["type"] = named_types[type_]
    for name, conf in config.items():
        if conf.get("default") == "__null__":
            conf["default"] = None
        try:
            conf["type"] = parse_schema(
                conf["type"], named_schemas=named_types, expand=True
            )
        except Exception as e:
            print(conf.get("name", "No Name"), e)
            conf = parse_schema(conf, named_schemas=named_types, expand=True)

    fields = []
    # give null as an option for fields with defaults
    for name, val in config.items():
        if "default" in val.keys() and not isinstance(val["type"], list):
            val["type"] = [val["type"], "null"]
        fields.append({"name": name} | val)
    avsc = {
        "type": "record",
        "name": "config",
        "fields": fields,
    }

    # print(json.dumps(avsc, indent=4, sort_keys=True))
    # step 2: convert to json schema using avrotize
    avrotize = subprocess.run(
        ["avrotize", "a2j"],
        input=json.dumps(avsc, indent=4, sort_keys=True),
        text=True,
        capture_output=True,
    )

    # step 3: curate/make tweaks to json schema
    try:
        schema = json.loads(avrotize.stdout)
    except Exception as e:
        print(avrotize.stdout)
        raise e

    def format_props(props):
        return {
            "type": "object",
            "properties": props,
            "required": [name for name in props.keys() if "default" not in props[name].keys()],
            "additionalProperties": False,
        }

    # now as a json schema, we can curate to better describe the toml requirements
    props = schema.pop("properties")

    # avrotize did not carry over defaults (why?); push them here
    for name, v in props.items():
        field = [d for d in avsc["fields"] if d["name"] == name]
        if field and "default" in field[0].keys():
            # filter limit fields to avoid infinity value
            new_val = field[0]["default"]
            if isinstance(new_val, list):
                if new_val == [-float("inf"), float("inf")]:
                    field[0]["default"] = [-1e300, 1e300]
            v["default"] = field[0]["default"]

    # daemon schema (schema will validate for python identifiers)
    schema["patternProperties"] = {r"^[a-zA-Z_][a-zA-Z0-9_]*$": format_props(props)}

    additional = format_props(props)
    additional["name"] = "shared-settings"
    additional.pop("required")

    schema["additionalProperties"] = additional
    schema["$schema"] = "http://json-schema.org/draft-04/schema"
    schema.pop("required")

    return schema
