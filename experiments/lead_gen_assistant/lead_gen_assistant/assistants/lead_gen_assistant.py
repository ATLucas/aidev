import json
from openai import OpenAI
import os
import time
from typing import Callable, Dict, List

from lead_gen_assistant.utils import ConsoleColor, write_yaml_config


class LeadGenAssistant:
    def __init__(
        self,
        config: Dict,
        instructions: str,
        tools: List[Dict],
        available_functions: Dict[str, Callable],
        get_user_input_callback: Callable,
    ):
        self._run_limit = config["settings"]["run_limit"]
        self._available_functions = available_functions
        self._get_user_input_callback = get_user_input_callback

        # API key is read automatically from the OPENAI_API_KEY evironment variable
        self._client = OpenAI()
        self._thread = None
        self._previous_message_id = None

        if "assistant_id" in config:
            self._assistant_id = config["assistant_id"]
            print(f"Loaded saved assistant ID: {self._assistant_id}")
        else:
            print("Creating new assistant")
            assistant = self._client.beta.assistants.create(
                name=LeadGenAssistant.__name__,
                instructions=instructions,
                model=config["settings"]["model"],
                tools=tools,
            )
            config["assistant_id"] = assistant.id
            write_yaml_config("assistant.yaml", config)
            self._assistant_id = assistant.id
            print(f"New assistant ID: {self._assistant_id}")

    def run(self) -> Dict:
        # Reset the run count
        self._run_count = 0

        # Create a new thread
        self._thread = self._client.beta.threads.create()

        # Get initial user message:
        user_input = self._get_user_input_callback()
        message = self._client.beta.threads.messages.create(
            thread_id=self._thread.id,
            role="user",
            content=user_input,
        )
        self._previous_message_id = message.id

        while True:
            if self._run_count >= self._run_limit:
                raise RunLimitExceeded()

            # Run on the thread
            run = self._client.beta.threads.runs.create(
                thread_id=self._thread.id,
                assistant_id=self._assistant_id,
            )
            run = self._wait_for_assistant(run)

            while run.required_action is not None and self._run_count < self._run_limit:
                tool_outputs = []

                # Check if GPT requested that any actions be run
                for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                    # Perform the action
                    action_response_message = self._perform_action(tool_call)
                    tool_outputs.append(action_response_message)

                if self._run_count >= self._run_limit:
                    raise RunLimitExceeded()

                # Add the action responses to the thread
                run = self._client.beta.threads.runs.submit_tool_outputs(
                    thread_id=self._thread.id, run_id=run.id, tool_outputs=tool_outputs
                )
                run = self._wait_for_assistant(run)

            # Get the user's response
            response = self._get_user_input_callback()

            # Add message to thread
            message = self._client.beta.threads.messages.create(
                thread_id=self._thread.id, role="user", content=response
            )
            self._previous_message_id = message.id

    def _wait_for_assistant(self, run):
        while run.status == "queued" or run.status == "in_progress":
            run = self._client.beta.threads.runs.retrieve(
                thread_id=self._thread.id,
                run_id=run.id,
            )
            time.sleep(0.5)
        show_json(run)
        self._print_new_messages()
        self._run_count += 1
        print(f"Run count: {self._run_count}")
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
        function_to_call = self._available_functions[function_name]
        function_args: Dict = json.loads(tool_call.function.arguments)
        function_response = function_to_call(**function_args)
        action_response_message = {
            "tool_call_id": tool_call.id,
            "output": function_response,
        }
        print(
            f"{ConsoleColor.CYAN}FUNCTION: {function_name}(**{function_args}) -> {function_response}{ConsoleColor.ENDCOLOR}\n"
        )
        return action_response_message


def show_json(obj):
    """Debugging helper that can be used on any assistants API object"""
    print(json.dumps(json.loads(obj.model_dump_json()), indent=2))


class RunLimitExceeded(Exception):
    def __init__(self, limit, message="Run limit exceeded"):
        self.limit = limit
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}: {self.limit}"
