import json
from typing import Dict, Any, List

from src.service.interface.arb_supporter.llm import LLM
from src.utils.constants import AGREE_PHRASES
from src.service.interface.arb_slave_agent.recognizer_agent import RecognizerAgent
from src.utils.constants import ConfirmationRecognizerAgentConfig

class ConfirmationRecognizerAgentImpl(RecognizerAgent):
    
    def __init__(
        self, 
        llm: LLM,
        model: str,
        name: str,
        task_description: str,
        report_config: Dict[str, Any],
        tools: List[Any]
    ) -> None:
        """
        Initialize the ConfirmationRecognizerAgentImpl with the given LLM, name, task description, agent configuration, report configuration, and tools.
        
        Args:
            llm (LLM): The LLM instance
            model (str): The model to use
            name (str): The name of the agent
            task_description (str): The description of the task
            report_config (Dict[str, Any]): The configuration for the report
            tools (List[Any]): The tools available to the agent
        """
        super(ConfirmationRecognizerAgentImpl, self).__init__()
        
        self.llm = llm
        self.model = model
        self.name = name
        self.task_description = task_description
        self.agent_config = ConfirmationRecognizerAgentConfig()
        self.format_schema = self.agent_config.format_schema
        self.system_prompt = self.agent_config.system_prompt
        self.user_prompt = self.agent_config.user_prompt
        self.instruction = self.agent_config.instruction
        self.few_shot = self.agent_config.few_shot
        self.report_config = report_config
        self.tools = tools


    def get_decision(
        self,
        query: str
    ) -> Dict[str, str]:
        
        agree_phrases = ", ".join(AGREE_PHRASES)

        user_prompt = self.user_prompt.format(
            query=query,
            instruction=self.instruction.format(
                agree_phrases=agree_phrases
            ),
            few_shot=self.few_shot
        )


        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = self.llm.invoke(
            messages=messages,
            format_schema=self.format_schema,
            model=self.model
        )
        if 'is_confirmed' in json.loads(response):
            return json.loads(response)['is_confirmed']
        
        return 0
