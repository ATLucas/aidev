from enum import Enum
import json
import os
import pkg_resources
from typing import Dict
import yaml


class ConsoleColor(Enum):
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    ENDCOLOR = "\033[0m"


def read_txt_config(filename: str):
    with open(get_resource_filepath(filename)) as file:
        return file.read()


def read_json_config(filename: str):
    with open(get_resource_filepath(filename)) as file:
        return json.load(file)


def read_yaml_config(filename: str):
    with open(get_resource_filepath(filename)) as file:
        return yaml.safe_load(file)


def write_txt_config(filename: str, data: str):
    with open(get_resource_filepath(filename), "w") as file:
        return file.write(data)


def write_json_config(filename: str, data: Dict):
    with open(get_resource_filepath(filename), "w") as file:
        return file.write(json.dumps(data, indent="2"))


def write_yaml_config(filename: str, data: Dict):
    with open(get_resource_filepath(filename), "w") as file:
        return yaml.dump(data, file)


def get_resource_filepath(filename) -> str:
    return pkg_resources.resource_filename(
        "lead_gen_assistant", os.path.join("config", filename)
    )
