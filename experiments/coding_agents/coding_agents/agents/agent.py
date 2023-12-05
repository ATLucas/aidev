# External
import json
from openai import OpenAI
import os
from typing import Callable, Dict, List

# Internal
from coding_agents.utils import DEBUG, MODEL_PRICING, ConsoleColor, ModelType, generate_agent_id


class Agent:
    def __init__(self, instructions: str, tools: Dict, actions: Dict[str, Callable], agent_id: str = None):
        self._instructions = instructions
        self._tools = tools
        self._actions = actions
        self._actions["record_memory"] = self._record_memory
        self._client = OpenAI()

        if agent_id is None:
            self._id = generate_agent_id()
            os.makedirs(f"agents_data/{self._id}", exist_ok=True)

        self._memory = self._read_memory()


    def perform_step(self, model: ModelType, user_prompt: str):
        total_cost = 0
        messages = [
            {
                "role": "system",
                "content": self._instructions.format(memory=self._memory),
            },
            {"role": "user", "content": user_prompt},
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

        if DEBUG:
            print(f"TOTAL COST: {total_cost}")

    def _read_memory(self):
        """
        Reads the memory of an AI agent from a file. If the file doesn't exist, 
        a default memory string is used.
        
        :return: A string containing the AI agent's memory.
        """
        file_path = f"agents_data/{self._id}/memory.md"
        default_memory = "This is the start of the conversation."

        try:
            # Check if the file exists
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
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
        :return: A JSON string with the operation result.
        """
        self._memory = memory

        directory = f"agents_data/{self._id}"
        file_path = f"{directory}/memory.md"

        try:
            # Create directory if it doesn't exist
            os.makedirs(directory, exist_ok=True)

            # Write memory to file
            with open(file_path, 'w') as file:
                file.write(memory)

            return json.dumps({"success": True, "message": f"Memory recorded successfully in '{file_path}'."})
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    def _query_model(self, model: ModelType, messages: List[Dict[str, str]]):
        # Send the query
        response = self._client.chat.completions.create(
            model=model.value,
            messages=messages,
            tools=self._tools,
            tool_choice="auto",
        )
        response_message = response.choices[0].message
        prompt_cost = response.usage.prompt_tokens * MODEL_PRICING[model]["prompt"] / 1000
        completion_cost = (
            response.usage.completion_tokens * MODEL_PRICING[model]["completion"] / 1000
        )
        total_cost = prompt_cost + completion_cost
        if DEBUG:
            print(f"PROMPT COST: {prompt_cost}")
            print(f"COMPLETION COST: {completion_cost}")
            print(f"TOTAL COST: {total_cost}")
        if response_message.content:
            print(f"\n{ConsoleColor.GREEN.value}Assistant: \n{response_message.content}{ConsoleColor.ENDCOLOR.value}\n")
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
        if DEBUG:
            print(
                f"{ConsoleColor.CYAN.value}FUNCTION: {function_name}(**{function_args}) -> {function_response}{ConsoleColor.ENDCOLOR.value}\n"
            )
        return action_response_message