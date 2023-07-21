import json
from os import path, mkdir


DIARYCLI_PATH   = "$HOME/.diarycli"
CONFIGS_FILE    = "configs.json"
CONFIGS_PATH    = f"{DIARYCLI_PATH}/{CONFIGS_FILE}"


def load_configs() -> dict:
    configs_path = path.expandvars(CONFIGS_PATH)

    if not path.exists(configs_path):
        restore_default()

    with open(configs_path) as f:
        data = json.load(f)

    if (data.get('storage') and not data.get('storage').endswith('/')):
        data['storage'] += '/'

    for key, val in data.items():
        if type(val) == str:
            data[key] = path.expandvars(val)
        else:
            data[key] = val

    return data

def update_configs(update_values: dict) -> dict:
    configs_path = path.expandvars(CONFIGS_PATH)
    configs = load_configs()
    configs.update(update_values)

    with open(configs_path, 'w') as f:
        f.write(json.dumps(configs, indent=4))

    return configs

def restore_default() -> dict:
    diarycli_path = path.expandvars(DIARYCLI_PATH)
    if (not path.exists(diarycli_path)):
        mkdir(diarycli_path)
        mkdir(f'{diarycli_path}/data')

    configs_path = path.expandvars(CONFIGS_PATH)

    configs = {
        "editor": "vi",
        "syncScript": f"{DIARYCLI_PATH}/scripts/sync_github.sh",
        "storage": f"{DIARYCLI_PATH}/data/",
        "saltLocation": f"{DIARYCLI_PATH}/.salt",
    }

    with open(configs_path, 'w') as f:
        f.write(json.dumps(configs, indent=4))

    return configs
