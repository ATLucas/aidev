# External
from abc import ABC, abstractmethod
from datetime import datetime
from openai import OpenAI
import os
from typing import Callable, Dict, Optional

# Internal
from coding_agents.utils import ConsoleColor, ModelType, generate_agent_id


class AgentInterface(ABC):
    def __init__(
        self,
        instructions: str,
        tools: Dict,
        actions: Dict[str, Callable],
        model: Optional[ModelType] = None,
        agent_id: Optional[str] = None,
    ):
        self._instructions = instructions
        self._tools = tools
        self._actions = actions
        self._model = model
        self._id = generate_agent_id() if agent_id is None else agent_id
        self._client = OpenAI()

        self._agent_data_dir = f"agents_data/{self._id}"
        self._chat_log_dir = f"{self._agent_data_dir}/chat_log"
        os.makedirs(self._chat_log_dir, exist_ok=True)

        datetimestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._chat_log_file = f"{self._chat_log_dir}/{datetimestamp}.log"

    @abstractmethod
    def perform_step(self, model: ModelType, user_request: str):
        pass

    def _log_chat(self, message: str):
        with open(self._chat_log_file, "a") as out_file:
            out_file.write(message)

    def _add_color(self, message: str, color: ConsoleColor) -> str:
        return f"{color.value}{message}{ConsoleColor.ENDCOLOR.value}"
