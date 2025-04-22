import json
from typing import List, Dict, Any


from src.utils.constants import NERAgentConfig
from src.service.interface.arb_supporter.llm import LLM
from src.service.interface.arb_slave_agent.ner_agent import NerAgent
from src.utils.utils import get_current_date, get_current_year, get_current_month

class NerAgentImpl(NerAgent):
    """
    Implementation of NerAgent using Ollama API for Named Entity Recognition.
    """
    
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
        Initialize the NerAgentImpl with Ollama API configuration.
        
        Args:
            llm (LLM): The LLM instance
            model (str): The model to use   
            name (str): The name of the agent
            task_description (str): The description of the task
            agent_config (NERAgentConfig): The configuration for the agent
            report_config (Dict[str, Any]): The configuration for the report
            tools (List[Any]): The tools available to the agent
        """
        super(NerAgentImpl, self).__init__()
        
        self.llm = llm
        self.model = model
        self.name = name
        self.task_description = task_description
        self.agent_config = NERAgentConfig()
        self.format_schema = self.agent_config.format_schema
        self.system_prompt = self.agent_config.system_prompt
        self.user_prompt = self.agent_config.user_prompt
        self.instruction = self.agent_config.instruction
        self.few_shot = self.agent_config.few_shot
        self.report_config = report_config
        self.tools = tools

    def __get_parameter_properties(self) -> str:
        parameter_properties = []
        for func_info in self.report_config:
            function_name = func_info['name']
            parameter_properties = func_info['parameters']['properties']
            for key, value in parameter_properties.items():
                if value['enum'] is None:
                    value2str = ", ".join(value['enum'])
                    format_schema = f"### {key.upper()}: {value2str}"
                    parameter_properties.append(format_schema)
            
        parameter_properties_to_string = "\n".join(parameter_properties)
        return parameter_properties_to_string

    def extract_entities(self, query: str) -> Dict[str, Any]:
        """
        Process the input text and extract named entities using Ollama API.
        
        Args:
            query (str): The input query to process
            
        Returns:
            Dict[str, Any]: Dictionary containing extracted entities and their metadata
        """
        
        parameter_properties = self.__get_parameter_properties()
        
        current_date = get_current_date()
        current_year = get_current_year()   
        current_month = get_current_month()
   
        user_prompt = self.user_prompt.format(
            query=query, 
            current_date=current_date,
            current_year=current_year,
            current_month=current_month,
            instruction=self.instruction.format(
                query=query,
                current_date=current_date,
                current_year=current_year,
                current_month=current_month,
                parameter_properties=parameter_properties
            ), 
            few_shot=self.few_shot.format(
                current_month=current_month,
                current_year=current_year,
            )
        )
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = self.llm.invoke(
            messages=messages,
            format_schema=self.format_schema,
            model=self.model,
            endpoint='/api/chat'
        )
        
        if not json.loads(response):
            return {
                "date_range": "N/A",
                "from_date": "N/A",
                "to_date": "N/A",
                "product": "All",
                "product_detail": "All",
                "level": "All",
                "user": "N/A"
            }
            
        return json.loads(response)