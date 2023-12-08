# External
import json
from openai import OpenAI
import os
import time
from typing import Callable, Dict

# Internal
from coding_agents.utils import DEBUG, ConsoleColor, ModelType, generate_agent_id


class Agent:
    def __init__(
        self,
        instructions: str,
        tools: Dict,
        actions: Dict[str, Callable],
        agent_id: str = None,
    ):
        self._instructions = instructions
        self._tools = tools
        self._actions = actions
        self._client = OpenAI()

        self._id = generate_agent_id() if agent_id is None else agent_id
        agent_data_dir = f"agents_data/{self._id}"
        assistant_id_file = f"{agent_data_dir}/assistant_id.txt"

        if agent_id is None:
            print("Creating new assistant")
            self._assistant = self._client.beta.assistants.create(
                name=self._id,
                instructions=instructions,
                tools=tools,
            )
            self._assistant_id = self._assistant.id
            os.makedirs(agent_data_dir, exist_ok=True)
            with open(assistant_id_file, "w") as out_file:
                out_file.write(f"{self._assistant.id}")
        else:
            print("Loading existing assistant")
            with open(assistant_id_file) as in_file:
                self._assistant_id = in_file.read()

        self._thread = self._client.beta.threads.create()

    def perform_step(self, model: ModelType, user_request: str):
        message = self._client.beta.threads.messages.create(
            thread_id=self._thread.id,
            role="user",
            content=user_request,
        )
        self._previous_message_id = message.id

        # Run on the thread
        run = self._client.beta.threads.runs.create(
            thread_id=self._thread.id,
            assistant_id=self._assistant_id,
            model=model.name,
        )
        run = self._wait_for_assistant(run)

        while run.required_action is not None:
            tool_outputs = []

            # Check if GPT requested that any actions be run
            for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                # Perform the action
                action_response_message = self._perform_action(tool_call)
                tool_outputs.append(action_response_message)

            # Add the action responses to the thread
            run = self._client.beta.threads.runs.submit_tool_outputs(
                thread_id=self._thread.id, run_id=run.id, tool_outputs=tool_outputs
            )
            run = self._wait_for_assistant(run)

    def _wait_for_assistant(self, run):
        while run.status == "queued" or run.status == "in_progress":
            run = self._client.beta.threads.runs.retrieve(
                thread_id=self._thread.id,
                run_id=run.id,
            )
            time.sleep(0.5)
        if DEBUG:
            show_json(run)
        self._print_new_messages()
        return run

    def _print_new_messages(self):
        messages = self._client.beta.threads.messages.list(
            thread_id=self._thread.id, order="asc", after=self._previous_message_id
        )
        for message in messages:
            print(
                f"{ConsoleColor.GREEN.value}{message.role.upper()}: "
                f"{message.content[0].text.value}{ConsoleColor.ENDCOLOR.value}\n"
            )
            self._previous_message_id = message.id

    def _perform_action(self, tool_call):
        function_name = tool_call.function.name
        function_to_call = self._actions[function_name]
        function_args: Dict = json.loads(tool_call.function.arguments)
        function_response = function_to_call(**function_args)
        action_response_message = {
            "tool_call_id": tool_call.id,
            "output": function_response,
        }
        if DEBUG:
            print(
                f"{ConsoleColor.CYAN.value}FUNCTION: {function_name}(**{function_args}) "
                f"-> {function_response}{ConsoleColor.ENDCOLOR.value}\n"
            )
        return action_response_message


def show_json(obj):
    """Debugging helper that can be used on any assistants API object"""
    print(json.dumps(json.loads(obj.model_dump_json()), indent=2))
