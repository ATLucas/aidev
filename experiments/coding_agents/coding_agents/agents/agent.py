# External
import json
from openai import OpenAI
from typing import Callable, Dict, List

# Internal
from coding_agents.utils import DEBUG, MODEL_PRICING, ConsoleColor, ModelType


class Agent:
    def __init__(self, instructions: str, tools: Dict, actions: Dict[str, Callable]):
        self._instructions = instructions
        self._tools = tools
        self._actions = actions
        self._client = OpenAI()
        
        # Check for existing ID
        # id_file_path = os.path.join(config_dir, "agent_id.txt")
        # if os.path.exists(id_file_path):
        #     with open(id_file_path, 'r') as file:
        #         self.id = file.read().strip()
        # else:
        #     self.id = generate_agent_id()
        #     with open(id_file_path, 'w') as file:
        #         file.write(self.id)

    def perform_step(self, model: ModelType, user_prompt: str):
        total_cost = 0
        messages = [
            {
                "role": "system",
                "content": self._instructions,
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