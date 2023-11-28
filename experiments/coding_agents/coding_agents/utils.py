from enum import Enum
import json
import openai
import os
from packaging import version
import pkg_resources
from typing import Dict
import yaml

REQUIRED_OPENAI_VERSION = "1.2.3"
DEBUG = True


class ConsoleColor(Enum):
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    ENDCOLOR = "\033[0m"


def validate_openai_version():
    # Check OpenAI version is correct
    required_version = version.parse(REQUIRED_OPENAI_VERSION)
    current_version = version.parse(openai.__version__)

    if current_version < required_version:
        raise ValueError(
            f"Error: OpenAI version {openai.__version__}"
            f" is less than the required version {REQUIRED_OPENAI_VERSION}"
        )
    else:
        print("OpenAI version is compatible.")


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
        "coding_agents", os.path.join("config", filename)
    )
