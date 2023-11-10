import json
from openai import OpenAI
import os
from typing import Dict, List

# Select your model:
MODEL = "gpt-4"  # GPT-4
# MODEL = "gpt-4-1106-preview"  # GPT-4 turbo preview
# MODEL = "gpt-3.5-turbo-1106"  # GPT-3 turbo

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

BLUE = "\033[94m"
GREEN = "\033[92m"
ENDCOLOR = "\033[0m"


# Define a function to communicate with OpenAI API
def main():
    client = OpenAI()

    print("You can start the conversation. Type 'quit' to exit.")

    while True:
        # To keep the context of the conversation small,
        # we will re-start the context for each user query.
        # This means that the agent will not know about
        # previous questions that you ask, but that's
        # acceptable for this experiment.
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

        # Get user input
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

        # Create the message for the API call
        messages.append({"role": "user", "content": user_message})

        # Ask the assistant
        assistant_message = ask_chatgpt(client, messages)
        print(f"{GREEN}Assistant: {assistant_message}{ENDCOLOR}")


def ask_chatgpt(client: OpenAI, messages: List[str]):
    initial_response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
    )
    response_message = initial_response.choices[0].message
    tool_calls = response_message.tool_calls
    print(f"INITIAL RESPONSE: \n{response_message}")

    while tool_calls:
        available_functions = {
            "agent_action_list_files": agent_action_list_files,
        }
        messages.append(response_message)

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args: Dict = json.loads(tool_call.function.arguments)
            arg_directory_name = function_args.get("directory_name")
            function_response = function_to_call(directory_name=arg_directory_name)
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )
            print(
                f"FUNCTION: \n{function_name}(directory_name={arg_directory_name}): \n{function_response}"
            )
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        print(f"RESPONSE: \n{response_message}")

    return response_message.content


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


if __name__ == "__main__":
    main()
