from enum import Enum
import importlib
import inspect
import json
import openai
import os
from packaging import version
import pkg_resources
import pkgutil
import random
from typing import Dict
import yaml

REQUIRED_OPENAI_VERSION = "1.2.3"
DEBUG = True


class ConsoleColor(Enum):
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    ENDCOLOR = "\033[0m"


class ModelType(Enum):
    GPT_4 = "gpt-4"
    GPT_4_turbo = "gpt-4-1106-preview"
    GPT_3_5_turbo = "gpt-3.5-turbo-1106"


# Dollars per 1000 tokens
MODEL_PRICING = {
    ModelType.GPT_4: {"prompt": 0.03, "completion": 0.06},
    ModelType.GPT_4_turbo: {"prompt": 0.01, "completion": 0.03},
    ModelType.GPT_3_5_turbo: {"prompt": 0.001, "completion": 0.002},
}


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


def get_available_actions(package_name: str) -> Dict:
    # Create an empty dictionary to hold the available actions
    available_actions = {}

    # Iterate over all the modules within the 'actions' package
    for _, module_name, _ in pkgutil.iter_modules(
        [os.path.join(package_name.replace(".", "/"))]
    ):
        # Import the module
        module = importlib.import_module(f"{package_name}.{module_name}")

        # Iterate over all items in the module
        for item_name in dir(module):
            item = getattr(module, item_name)
            # Check if the item is a function and not a built-in function
            if inspect.isfunction(item) and item.__module__ == module.__name__:
                available_actions[item_name] = item

    return available_actions


# Sample list of adjectives and nouns for generating human-readable names
unique_names = None


def generate_agent_id():
    """
    Generates a human-readable and somewhat unique ID by combining
    a random adjective, a random noun, and a random number.
    """
    global unique_names

    if unique_names is None:
        unique_names = read_yaml_config("unique_names.yaml")

    adjective = random.choice(unique_names["adjectives"])
    noun = random.choice(unique_names["nouns"])
    unique_number = random.randint(100, 999)  # Random number for added uniqueness
    return f"{adjective}-{noun}-{unique_number}"
