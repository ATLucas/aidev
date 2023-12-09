# External
import json
import os
from typing import Callable, Dict, List, Optional

# Internal
from coding_agents.agents.agent_interface import AgentInterface
from coding_agents.utils import (
    DEBUG,
    MODEL_PRICING,
    ConsoleColor,
    ModelType,
    read_txt_config,
)


class AgentLatentSpace(AgentInterface):
    def __init__(
        self,
        instructions: str,
        tools: Dict,
        actions: Dict[str, Callable],
        model: Optional[ModelType] = None,
        agent_id: Optional[str] = None,
    ):
        super().__init__(instructions, tools, actions, model, agent_id)
        self._user_prompt = read_txt_config("agent/user_prompt.md")
        self._memory_prompt = read_txt_config("agent/memory_prompt.md")
        self._memory_data_file = f"{self._agent_data_dir}/memory.md"
        self._memory = self._read_memory()

    def perform_step(self, model: ModelType, user_request: str):
        total_cost = 0
        self._log_chat(f"MEMORY: {self._memory}\n")
        self._log_chat(f"USER: {user_request}\n")
        user_message_content = self._user_prompt.format(
            memory=self._memory, user_request=user_request
        )
        messages = [
            {"role": "system", "content": self._instructions},
            {"role": "user", "content": user_message_content},
        ]

        # Query model
        response_message, cost = self._query_model(model, messages)
        total_cost += cost

        while response_message.tool_calls:
            # Add GPT's response to the list of messages
            # for GPT to use in the next query
            messages.append(response_message)

            # Check if GPT requested that any actions be run
            for tool_call in response_message.tool_calls:
                action_response_message = self._perform_action(tool_call)

                # Add the action response to the list of messages for the model to use
                messages.append(action_response_message)

            # Query model again
            response_message, cost = self._query_model(model, messages)
            total_cost += cost

        # Prompt AI to generate memory
        messages.append({"role": "user", "content": self._memory_prompt})

        # Query model for updated memory content
        if DEBUG:
            print("QUERYING MODEL FOR MEMORY")

        # Always use GPT_3_5_turbo to generate the memory,
        # since it is a relatively simple summarization task.
        response_message, cost = self._query_model(ModelType.GPT_3_5_turbo, messages)
        total_cost += cost

        # Write the updated memory content to file
        self._memory = response_message.content
        if DEBUG:
            print(f"MEMORY: {self._memory}")
        if self._memory:
            self._record_memory(self._memory)

        log_content = f"STEP TOTAL COST: {total_cost}\n"
        self._log_chat(log_content)
        print(log_content)

    def _read_memory(self) -> str:
        """
        Reads the memory of an AI agent from a file. If the file doesn't exist,
        a default memory string is used.

        :return: A string containing the AI agent's memory.
        """
        default_memory = "This is the start of the conversation."

        try:
            if os.path.exists(self._memory_data_file):
                with open(self._memory_data_file, "r") as file:
                    return file.read()
            else:
                return default_memory
        except Exception as e:
            print(f"Error reading memory file: {e}")
            return default_memory

    def _record_memory(self, memory: str):
        """
        Records the memory of an AI agent to a file.

        :param memory: A string containing the AI agent's memory.
        """
        self._memory = memory
        with open(self._memory_data_file, "w") as file:
            file.write(memory)

    def _query_model(self, model: ModelType, messages: List[Dict[str, str]]):
        # Send the query
        response = self._client.chat.completions.create(
            model=model.value,
            messages=messages,
            tools=self._tools,
            tool_choice="auto",
        )
        response_message = response.choices[0].message
        prompt_cost = (
            response.usage.prompt_tokens * MODEL_PRICING[model]["prompt"] / 1000
        )
        completion_cost = (
            response.usage.completion_tokens * MODEL_PRICING[model]["completion"] / 1000
        )
        total_cost = prompt_cost + completion_cost
        for log_content in (
            f"QUERY PROMPT COST: {prompt_cost}\n",
            f"QUERY COMPLETION COST: {completion_cost}\n",
            f"QUERY COST: {total_cost}\n",
        ):
            self._log_chat(log_content)
            print(log_content)
        if response_message.content:
            log_content = f"ASSISTANT: {response_message.content}\n"
            self._log_chat(log_content)
            print(self._add_color(log_content, ConsoleColor.GREEN))
        return response_message, total_cost

    def _perform_action(self, tool_call):
        function_name = tool_call.function.name
        function_to_call = self._actions[function_name]
        function_args: Dict = json.loads(tool_call.function.arguments)
        function_response = function_to_call(**function_args)
        action_response_message = {
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": function_name,
            "content": function_response,
        }
        log_content = (
            f"FUNCTION: {function_name}({function_args}) -> {function_response}\n"
        )
        self._log_chat(log_content)
        print(self._add_color(log_content, ConsoleColor.CYAN))
        return action_response_message
