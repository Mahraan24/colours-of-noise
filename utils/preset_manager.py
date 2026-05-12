import json
import os
import config as cg

PRESETS_FILE = "presets.json"

def load() -> dict:
    if not os.path.exists(PRESETS_FILE):
        return {}
    try:
        with open(PRESETS_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def write(presets: dict):
    with open(PRESETS_FILE, "w") as f:
        json.dump(presets, f, indent=4)

def save(name: str, data: dict) -> tuple[bool, str]:
    presets = load()
    if name in presets:
        return False, "Present already exists."
    if len(presets) >= cg.max_presets:
        return False, f"Maximum of {cg.max_presets} presets."
    presets[name] = data
    write(presets)
    return True, "Preset saved."

def delete(name: str) -> tuple[bool, str]:
    presets = load()
    if name not in presets:
        return False, "Preset not found."
    del presets[name]
    write(presets)
    return True, "Preset deleted."