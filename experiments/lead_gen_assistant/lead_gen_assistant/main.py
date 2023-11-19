from lead_gen_assistant.data_saver import DataSaver
from lead_gen_assistant.assistants.basic_assistant import BasicAssistant
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
    data_saver = DataSaver()
    BasicAssistant(
        config=read_yaml_config("assistant.yaml"),
        instructions=read_txt_config("instructions.txt"),
        tools=read_yaml_config("tools.yaml"),
        available_functions={
            "save_name": data_saver.save_name,
            "save_email": data_saver.save_email,
            "save_phone_number": data_saver.save_phone_number,
            "save_budget": data_saver.save_budget,
            "save_investment_goal": data_saver.save_investment_goal,
            "save_property_type": data_saver.save_property_type,
            "save_property_count": data_saver.save_property_count,
            "save_referral_source": data_saver.save_referral_source,
            "save_referrer_name": data_saver.save_referrer_name,
        },
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


if __name__ == "__main__":
    main()
