from typing import Dict, Any, List

from src.service.interface.arb_slave_agent.greeting_agent import GreetingAgent
from src.service.interface.arb_supporter.llm import LLM
from src.service.implement.arb_supporter_impl.prompt_impl import GreetingAgentConfig

class GreetingAgentImpl(GreetingAgent):
    
    def __init__(
        self,
        llm: LLM,
        model: str,
        name: str,
        task_description: str,
        report_config: Dict[str, Any],
        agent_config: GreetingAgentConfig,
        tools: List[Any]
    ) -> None:
        """
        Initialize the GreetingAgentImpl with the given LLM, name, task description, agent configuration, report configuration, and tools.
        
        Args:
            llm (LLM): The LLM instance
            model (str): The model to use
            name (str): The name of the agent
            task_description (str): The description of the task
            report_config (Dict[str, Any]): The configuration for the report
            tools (List[Any]): The tools available to the agent
        """
        super(GreetingAgentImpl, self).__init__()
        
        self.llm = llm
        self.model = model
        self.name = name
        self.task_description = task_description
        self.agent_config = agent_config()
        self.system_prompt = self.agent_config.system_prompt
        self.report_config = report_config
        self.tools = tools
       
    def __repr__(self) -> str:
        return f"{self.name}: {self.task_description}"
    
    def chat(self, message: str) -> str:
        
        user_prompt = self.agent_config.format_prompt(message=message)

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = self.llm.invoke(
            messages=messages,
            model=self.model
        )
        
        return response