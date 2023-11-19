from newsletter_va.data_saver import DataSaver
from newsletter_va.assistants.basic_assistant import BasicAssistant
from newsletter_va.utils import (
    ConsoleColor,
    read_txt_config,
    read_yaml_config,
    validate_openai_version,
)


def main():
    validate_openai_version()
    data_saver = DataSaver()
    BasicAssistant(
        config=read_yaml_config("assistant.yaml"),
        instructions=read_txt_config("instructions.txt"),
        tools=read_yaml_config("tools.yaml"),
        available_functions={
            "save_interests": data_saver.save_interests,
            "save_industry": data_saver.save_industry,
            "save_occupation": data_saver.save_occupation,
            "save_coding_skill_level": data_saver.save_coding_skill_level,
            "save_professional_goals": data_saver.save_professional_goals,
            "save_referral_source": data_saver.save_referral_source,
            "save_region_or_timezone": data_saver.save_region_or_timezone,
            "save_feedback": data_saver.save_feedback,
        },
        get_user_input_callback=get_user_input,
    ).run()


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
