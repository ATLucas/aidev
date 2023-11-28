from coding_agents.assistants.basic_assistant import BasicAssistant
from coding_agents.functions.find_file import find_file
from coding_agents.functions.read_file import read_file
from coding_agents.functions.write_file import write_file
from coding_agents.utils import ConsoleColor, validate_openai_version


def main():
    validate_openai_version()
    BasicAssistant(
        config_dir="sw_design_assistant",
        available_functions={
            "find_file": find_file,
            "read_file": read_file,
            "write_file": write_file,
        },
        get_user_input_callback=get_user_input,
    ).run()


def get_user_input() -> str:
    """Callback that agent can use to get input from its user"""
    try:
        user_input = input(f"{ConsoleColor.BLUE.value}You: ")
        if user_input == "quit":
            raise ValueError("User requested quit")
        print(f"{ConsoleColor.ENDCOLOR.value}")
        return user_input
    except:
        print(f"{ConsoleColor.ENDCOLOR.value}")
        raise


if __name__ == "__main__":
    main()
