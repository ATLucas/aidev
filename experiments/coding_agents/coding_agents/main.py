from coding_agents.agents.basic_agent import BasicAgent
from coding_agents.utils import ConsoleColor, get_available_functions, validate_openai_version


def main():
    validate_openai_version()
    BasicAgent(
        config_dir="sw_design_assistant",
        available_functions=get_available_functions("coding_agents.functions"),
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
