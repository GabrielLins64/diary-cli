import json
from os import path


DIARYCLI_PATH   = "$HOME/.diarycli"
CONFIGS_FILE    = "configs.json"
CONFIGS_PATH    = f"{DIARYCLI_PATH}/{CONFIGS_FILE}"


def load_configs() -> dict:
    configs_path = path.expandvars(CONFIGS_PATH)

    if not path.exists(configs_path):
        restore_default()

    with open(configs_path) as f:
        data = json.load(f)

    for key, val in data.items():
        data[key] = path.expandvars(val)

    return data

def update_configs(update_values: dict) -> dict:
    configs_path = path.expandvars(CONFIGS_PATH)
    configs = load_configs()
    configs.update(update_values)

    with open(configs_path, 'w') as f:
        f.write(json.dumps(configs, indent=4))

    return configs

def restore_default() -> dict:
    configs_path = path.expandvars(CONFIGS_PATH)

    configs = {
        "editor": "vi",
        "syncScript": f"{DIARYCLI_PATH}/scripts/sync_github.sh",
        "storage": f"{DIARYCLI_PATH}/data/"
    }

    with open(configs_path, 'w') as f:
        f.write(json.dumps(configs, indent=4))

    return configs
