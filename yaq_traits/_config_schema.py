"""create config schema validation"""

import json
from fastavro import parse_schema
import subprocess


def main(avpr):
    config = avpr["config"]

    # step 1: make a valid avro protocol for the config
    named_types = {ty["name"]: ty for ty in avpr.get("types", [])}
    # rerunning parsing to expand types
    for name, conf in config.items():
        if conf.get("default") == "__null__":
            conf["default"] = None
        try:
            conf["type"] = parse_schema(conf["type"], named_schemas=named_types, expand=True)
        except:
            parse_schema(conf, named_schemas=named_types, expand=True)
    # complex types cast as dictionaries
    # also needed for others (map, record?)???
    for k, v in config.items():
        if v["type"] == "array":
            config[k]["type"] = {"type": "array", **v}
        elif v["type"] == "enum":
            config[k]["type"] = {"type": "enum", **v}

    fields = []
    for name, val in config.items():
        if "default" in val.keys() and not isinstance(val["type"], list):
            val["type"] = [val["type"], "null"]
        fields.append({"name": name} | val)
    avsc = {
        "type": "record",
        "name": "config",
        "fields": fields,
    }

    # step 2: convert to json schema using avrotize
    avrotize = subprocess.run(
        ["avrotize", "a2j"],
        input=json.dumps(avsc, indent=4, sort_keys=True),
        text=True,
        capture_output=True,
    )

    # step 3: curate/make tweaks to json schema
    schema = json.loads(avrotize.stdout)

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
            # hope is that limit default becomes something else (none, none)?, and infinite bounds are assumed in code
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
    schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    schema.pop("required")

    return schema
