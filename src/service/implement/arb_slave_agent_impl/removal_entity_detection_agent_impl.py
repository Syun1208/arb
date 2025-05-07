from typing import Any, Dict, List
import json

from src.service.interface.arb_slave_agent.removal_entity_detection_agent import RemovalEntityDetectionAgent
from src.service.interface.arb_supporter.llm import LLM
from src.service.implement.arb_supporter_impl.prompt_impl import RemovalEntityDetectionAgentConfig


class RemovalEntityDetectionAgentImpl(RemovalEntityDetectionAgent):
    
    """
    Implementation of RemovalEntityDetectionAgent using Ollama API for Removal Entity Detection.    
    """
    
    def __init__(
        self,
        llm: LLM,
        model: str, 
        name: str,
        task_description: str,
        report_config: Dict[str, Any],
        agent_config: RemovalEntityDetectionAgentConfig,
        tools: List[Any]
    ) -> None:
        """
        Initialize the RemovalEntityDetectionAgentImpl with Ollama API configuration.
        
        Args:
            llm (LLM): The LLM instance
            model (str): The model to use   
            name (str): The name of the agent
            task_description (str): The description of the task
            agent_config (NERAgentConfig): The configuration for the agent
            report_config (Dict[str, Any]): The configuration for the report
            tools (List[Any]): The tools available to the agent
        """
        super(RemovalEntityDetectionAgentImpl, self).__init__()
        
        self.llm = llm
        self.model = model
        self.name = name
        self.task_description = task_description
        self.agent_config = agent_config()
        self.report_config = report_config
        self.tools = tools
    
    def __repr__(self) -> str:
        return f"{self.name}: {self.task_description}"
    
        
    def detect_removal_entities(self, message: str, entities: Dict[str, str]) -> List[str]:
        
        key_entities = list(entities.keys())
        self.agent_config.update_format_schema(key_entities)
        
        user_prompt = self.agent_config.format_prompt(
            message=message,
            entities=entities
        )
        
        messages = [
            {"role": "system", "content": self.agent_config.system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = self.llm.invoke(
            messages=messages, 
            format_schema=self.agent_config.format_schema,
            model=self.model
        )
        
        if 'params2delete' in json.loads(response):
            return json.loads(response)['params2delete']
        
        return []
        
        
        
        
        
        
        


