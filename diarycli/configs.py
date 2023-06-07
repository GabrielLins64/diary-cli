import json


CONFIGS_PATH = "configs.json"


def load_configs() -> dict:
    with open(CONFIGS_PATH) as f:
        data = json.load(f)

    return data

def update_configs(update_values: dict) -> dict:
    configs = load_configs()
    configs.update(update_values)

    with open(CONFIGS_PATH, 'w') as f:
        f.write(json.dumps(configs, indent=4))

    return configs

def restore_default() -> dict:
    configs = {
        "editor": "vi",
        "syncScript": "~/.diarycli/scripts/sync_github.sh",
        "storage": "~/.diarycli/data/"
    }

    with open(CONFIGS_PATH, 'w') as f:
        f.write(json.dumps(configs, indent=4))

    return configs
