from coding_agents.agents.agent_latent_space import AgentLatentSpace
from coding_agents.agents.agent_assistants_api import AgentAssistantsApi
from coding_agents.utils import (
    ConsoleColor,
    ModelType,
    get_available_actions,
    read_txt_config,
    read_yaml_config,
    validate_openai_version,
)

# MODEL = ModelType.GPT_3_5_turbo
MODEL = ModelType.GPT_4_turbo
# MODEL = ModelType.GPT_4


def main():
    validate_openai_version()
    coder_agent = AgentLatentSpace(
        instructions=read_txt_config("coder_agent/instructions.md"),
        tools=read_yaml_config("coder_agent/tools.yaml"),
        actions=get_available_actions("coding_agents.actions"),
        model=MODEL,
    )

    while True:
        try:
            user_prompt = input(f"{ConsoleColor.BLUE.value}You: ")
            if user_prompt == "quit":
                break
            print(f"{ConsoleColor.ENDCOLOR.value}")
        except:
            print(f"{ConsoleColor.ENDCOLOR.value}")
            raise

        coder_agent.perform_step(MODEL, user_prompt)


if __name__ == "__main__":
    main()
