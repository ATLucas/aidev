from typing import Dict
from lead_gen_assistant.assistants.lead_gen_assistant import LeadGenAssistant
from lead_gen_assistant.utils import (
    ConsoleColor,
    read_txt_config,
    read_yaml_config,
)
import openai
from packaging import version

REQUIRED_OPENAI_VERSION = "1.2.3"


def main():
    validate_openai_version()
    LeadGenAssistant(
        config=read_yaml_config("assistant.yaml"),
        instructions=read_txt_config("instructions.txt"),
        tools=read_yaml_config("tools.yaml"),
        available_functions={"save_result": save_result},
        get_user_input_callback=get_user_input,
    ).run()


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


def get_user_input() -> str:
    """Callback that agent can use to get input from its user"""
    try:
        user_input = input(f"{ConsoleColor.BLUE.value}You: ")
        print(f"{ConsoleColor.ENDCOLOR.value}")
        return user_input
    except:
        print(f"{ConsoleColor.ENDCOLOR.value}")
        raise


def save_result(result: Dict):
    """Save the result returned by GPT"""
    print(f"RESULT: {result}")


if __name__ == "__main__":
    main()
