from enum import Enum
import json
from openai import OpenAI
import os
from typing import Dict, List


class ModelType(Enum):
    GPT_4 = "gpt-4"
    GPT_4_turbo_preview = "gpt-4-1106-preview"
    GPT_3_5_turbo = "gpt-3.5-turbo-1106"


# Choose your model
MODEL = ModelType.GPT_3_5_turbo

MODEL_PRICING = {
    ModelType.GPT_4: 0.03,
    ModelType.GPT_4_turbo_preview: 0.01,
    ModelType.GPT_3_5_turbo: 0.001,
}

SYSTEM_PROMPT = """
# Role

You are a file retrieval agent responsible for answering queries about files in a particular local git repo.

# Context

You will work within the root of the git repo as your current working directory.
You will be provided the ability to list the contents of any directory within the repo.

# Mission

Answer any user queries about the files in the repo.
For example, if the user asks what directory test.txt is in,
you will respond with the correct directory or directories containing a file called test.txt.

# Method

In order to fulfill the user requests efficiently and accurately, you are to iteratively operate using the following steps:
1. THINK: Think or plan about what actions you need to take to fulfill the user request.
2. ACT: Act out your plan using the provided function(s).
3. OBSERVE: Observe the results of your actions to determine whether the objective can now be met or whether another iteration of THINK-ACT-OBSERVE needs to be performed.

# Summary

Please operate within the provided role and context to complete your mission with the specified method.
Show your chain of reasoning and provide your final response to the user.

"""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "agent_action_list_files",
            "description": "List the files and directories in the specified directory",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory_name": {
                        "type": "string",
                        "description": "The name of the directory to list the contents of",
                    },
                },
                "required": ["directory_name"],
            },
        },
    }
]


def agent_action_list_files(directory_name: str):
    directory_name = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", directory_name
    )
    file_list: List[str] = []
    for file_name in os.listdir(directory_name):
        full_file_path = os.path.join(directory_name, file_name)
        file_type = "FILE" if os.path.isfile(file_name) else "DIR"
        file_list.append(f"{file_type}: {full_file_path}")
    return "\n".join(file_list)


AVAILABLE_FUNCTIONS = {
    "agent_action_list_files": agent_action_list_files,
}

BLUE = "\033[94m"
GREEN = "\033[92m"
ENDCOLOR = "\033[0m"

CLIENT = OpenAI()


# Define a function to communicate with OpenAI API
def main():
    print("You can start the conversation. Type 'quit' to exit.")

    while True:
        # To keep the context of the conversation small,
        # we will re-start the context for each user query.
        # This means that the agent will not know about
        # previous questions that you ask, but that is
        # acceptable for this experiment.
        try:
            user_message = input(f"{BLUE}You: ")
            print(f"{ENDCOLOR}")
        except:
            print(f"{ENDCOLOR}")
            raise

        # Check if the user wants to quit the conversation
        if user_message.lower() == "quit":
            print("Exiting conversation.")
            break

        # Ask the assistant
        assistant_message = ask_chatgpt(user_message)
        print(f"{GREEN}Assistant: {assistant_message}{ENDCOLOR}")


def ask_chatgpt(user_message: str):
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {"role": "user", "content": user_message},
    ]

    # Query GPT
    response_message = query_chatgpt(messages)

    while response_message.tool_calls:
        # Add GPT's response to the list of messages
        # for GPT to use in the next query
        messages.append(response_message)

        # Check if GPT requested that any actions be run
        for tool_call in response_message.tool_calls:
            action_response_message = perform_action(tool_call)

            # Add the action response to the list of messages
            # for GPT to use
            messages.append(action_response_message)

        # Query GPT again
        response_message = query_chatgpt(messages)

    return response_message.content


def query_chatgpt(messages: List[Dict[str, str]]):
    # Before sending the query, count the tokens that will be used:
    num_tokens = 0
    for message in messages:
        if isinstance(message, Dict):
            for value in message.values():
                num_tokens += count_tokens(value)
        else:
            num_tokens += count_tokens(message.content)

    dollars_per_1000_tokens = MODEL_PRICING[MODEL]
    total_cost = num_tokens * dollars_per_1000_tokens / 1000.0
    print(f"QUERY: {num_tokens=}, ${total_cost=}")

    # Send the query
    response = CLIENT.chat.completions.create(
        model=MODEL.value,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
    )
    response_message = response.choices[0].message
    print(f"RESPONSE: \n{response_message.content}\n")
    return response_message


def count_tokens(message: str) -> float:
    return 0


def perform_action(tool_call):
    function_name = tool_call.function.name
    function_to_call = AVAILABLE_FUNCTIONS[function_name]
    function_args: Dict = json.loads(tool_call.function.arguments)
    arg_directory_name = function_args.get("directory_name")
    function_response = function_to_call(directory_name=arg_directory_name)
    action_response_message = {
        "tool_call_id": tool_call.id,
        "role": "tool",
        "name": function_name,
        "content": function_response,
    }
    print(
        f"FUNCTION: \n{function_name}(directory_name={arg_directory_name}): \n{function_response}\n"
    )
    return action_response_message


if __name__ == "__main__":
    main()
