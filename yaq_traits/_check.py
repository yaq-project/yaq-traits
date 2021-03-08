__all__ = ["check"]


from .__traits__ import traits
from ._compose import compose


def check_trait(avpr, trait):
    gold = compose({"traits": [trait]})
    # config
    for config, v in gold.get("config", {}).items():
        if config not in avpr.get("config", {}).keys():
            return False
        if v["type"] != avpr["config"][config]["type"]:
            return False
    # state
    for state, v in gold.get("state", {}).items():
        if state not in avpr.get("state", {}).keys():
            return False
        if v["type"] != avpr["state"][state]["type"]:
            return False
    # messages
    for message, v in gold.get("messages", {}).items():
        if message not in avpr["messages"].keys():
            return False
        for i, r in enumerate(v.get("request", [])):
            if r["type"] != avpr["messages"][message]["request"][i]["type"]:
                return False
        if v.get("response", {}) != avpr["messages"][message].get("response", {}):
            return False
    # success!
    return True


def check(avpr):
    out = dict()
    # check state defaults
    for k, state in avpr.get("state", {}).items():
        if "default" not in state:
            raise Exception(f'state item "{k}" has no default')
    # check traits
    for trait in traits.keys():
        out[trait] = check_trait(avpr, trait)
    return out
