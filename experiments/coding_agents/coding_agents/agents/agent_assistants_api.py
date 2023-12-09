# External
from datetime import datetime
import json
import os
import time
from typing import Callable, Dict, Optional

# Internal
from coding_agents.agents.agent_interface import AgentInterface
from coding_agents.utils import DEBUG, ConsoleColor, ModelType


class AgentAssistantsApi(AgentInterface):
    def __init__(
        self,
        instructions: str,
        tools: Dict,
        actions: Dict[str, Callable],
        model: Optional[ModelType] = None,
        agent_id: Optional[str] = None,
    ):
        super().__init__(instructions, tools, actions, model, agent_id)
        assistant_id_file = f"{self._agent_data_dir}/assistant_id.txt"

        if os.path.exists(assistant_id_file):
            print("Loading existing assistant")
            with open(assistant_id_file) as in_file:
                self._assistant_id = in_file.read()
        else:
            print("Creating new assistant")
            self._assistant = self._client.beta.assistants.create(
                name=self._id,
                instructions=self._instructions,
                tools=self._tools,
                model=self._model.value,  # Overridden in perform_step
            )
            self._assistant_id = self._assistant.id

            with open(assistant_id_file, "w") as out_file:
                out_file.write(f"{self._assistant.id}")

        self._thread = self._client.beta.threads.create()

    def perform_step(self, model: ModelType, user_request: str):
        self._log_chat(f"USER: {user_request}\n")
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
            model=model.value,
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
            log_content = f"{message.role.upper()}: {message.content[0].text.value}\n"
            self._log_chat(log_content)
            print(self._add_color(log_content, ConsoleColor.GREEN))
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
        log_content = (
            f"FUNCTION: {function_name}({function_args}) -> {function_response}\n"
        )
        self._log_chat(log_content)
        print(self._add_color(log_content, ConsoleColor.CYAN))
        return action_response_message


def show_json(obj):
    """Debugging helper that can be used on any assistants API object"""
    print(json.dumps(json.loads(obj.model_dump_json()), indent=2))
