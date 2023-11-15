from enum import Enum
import json
import os
import time
from typing import Dict
from openai import OpenAI

CLIENT = OpenAI()


class ModelType(Enum):
    GPT_4 = "gpt-4"
    GPT_4_turbo_preview = "gpt-4-1106-preview"
    GPT_3_5_turbo = "gpt-3.5-turbo-1106"


# Choose your model
MODEL = ModelType.GPT_3_5_turbo

# Dollars per 1000 tokens
MODEL_PRICING = {
    ModelType.GPT_4: {"prompt": 0.03, "completion": 0.06},
    ModelType.GPT_4_turbo_preview: {"prompt": 0.01, "completion": 0.03},
    ModelType.GPT_3_5_turbo: {"prompt": 0.001, "completion": 0.002},
}

SYSTEM_PROMPT = """
# Role

You are a file browsing agent responsible for answering queries about files in a particular local git repo.

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
            "description": "List the files and directories in the specified directory within the repository",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory_name": {
                        "type": "string",
                        "description": "The name of the directory within the repository to list the contents of",
                    },
                },
                "required": ["directory_name"],
            },
        },
    },
    {"type": "code_interpreter"},
]

REPO_ROOT = os.path.relpath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Max number of iterations to allow the assistent to perform (limits cost)
RUN_LIMIT = 10


def agent_action_list_files(directory_name: str):
    # Safety check
    if directory_name and directory_name[0] == "/":
        return ""

    actual_dir_path = os.path.join(REPO_ROOT, directory_name)

    if not os.path.isdir(actual_dir_path):
        return ""

    files = []
    for file_name in os.listdir(actual_dir_path):
        actual_file_path = os.path.join(actual_dir_path, file_name)
        agent_file_path = os.path.join(directory_name, file_name)
        file_type = "DIR" if os.path.isdir(actual_file_path) else "FILE"
        files.append({"file_type": file_type, "file_path": agent_file_path})
    return json.dumps({"files": files})


AVAILABLE_FUNCTIONS = {
    "agent_action_list_files": agent_action_list_files,
}

BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
ENDCOLOR = "\033[0m"


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
        ask_chatgpt(user_message)


def ask_chatgpt(user_message: str):
    # Create assistant
    assistant = CLIENT.beta.assistants.create(
        name="File Browser Bot",
        instructions=SYSTEM_PROMPT,
        tools=TOOLS,
        model=MODEL.value,
    )

    # Create thread
    thread = CLIENT.beta.threads.create()

    # Add user message to thread
    message = CLIENT.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message,
    )
    previous_message_id = message.id

    # Run the thread
    run = CLIENT.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )
    run = wait_for_assistant(thread, run)
    # print("\nRUN OBJECT:")
    # show_json(run)
    run_count = 1

    # Print new messages
    messages = CLIENT.beta.threads.messages.list(
        thread_id=thread.id, order="asc", after=previous_message_id
    )
    for message in messages:
        print(
            f"{GREEN}{message.role.upper()}: {message.content[0].text.value}{ENDCOLOR}\n"
        )
        previous_message_id = message.id

    # last_message = user_message

    while run.required_action is not None and run_count < RUN_LIMIT:
        tool_outputs = []

        # Check if GPT requested that any actions be run
        for tool_call in run.required_action.submit_tool_outputs.tool_calls:
            # Perform the action
            action_response_message = perform_action(tool_call)
            tool_outputs.append(action_response_message)
            run_count += 1

        # Add the action responses to the thread
        run = CLIENT.beta.threads.runs.submit_tool_outputs(
            thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs
        )
        run = wait_for_assistant(thread, run)
        # print("\nRUN OBJECT:")
        # show_json(run)

        # Print new messages
        messages = CLIENT.beta.threads.messages.list(
            thread_id=thread.id, order="asc", after=previous_message_id
        )
        for message in messages:
            print(
                f"{GREEN}{message.role.upper()}: {message.content[0].text.value}{ENDCOLOR}\n"
            )
            previous_message_id = message.id

    # print("\nALL MESSAGES:")
    # messages = CLIENT.beta.threads.messages.list(thread_id=thread.id, order="asc")
    # for message in messages:
    #     print(f"{message.role.upper()}: {message.content[0].text.value}")


def wait_for_assistant(thread, run):
    while run.status == "queued" or run.status == "in_progress":
        run = CLIENT.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run


def perform_action(tool_call):
    function_name = tool_call.function.name
    function_to_call = AVAILABLE_FUNCTIONS[function_name]
    function_args: Dict = json.loads(tool_call.function.arguments)
    arg_directory_name = function_args.get("directory_name")
    function_response = function_to_call(directory_name=arg_directory_name)
    action_response_message = {
        "tool_call_id": tool_call.id,
        "output": function_response,
    }
    print(
        f"{CYAN}FUNCTION: {function_name}(directory_name={arg_directory_name}) -> {function_response}{ENDCOLOR}\n"
    )
    return action_response_message


def show_json(obj):
    """Debugging helper that can be used on any assistants API object"""
    print(json.dumps(json.loads(obj.model_dump_json()), indent=2))


if __name__ == "__main__":
    main()
