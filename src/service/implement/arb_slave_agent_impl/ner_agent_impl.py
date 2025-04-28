import json
from typing import List, Dict, Any


from src.service.interface.arb_supporter.llm import LLM
from src.service.interface.arb_slave_agent.ner_agent import NerAgent
from src.service.implement.arb_supporter_impl.prompt_impl import NerAgentConfig
from src.utils.utils import flatten_list_2d

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
        agent_config: NerAgentConfig,
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
        self.agent_config = agent_config()
        self.report_config = report_config
        self.tools = tools
        
        
    def __repr__(self) -> str:
        return f"{self.name}: {self.task_description}"
    
    
    def __get_parameter_properties(self, function_called: str) -> str:
        func_info = self.report_config[function_called]
        
        parameter_info = []
        parameter_properties = func_info['function']['parameters']['properties']
        for key, value in parameter_properties.items():
                if value['enum'] is not None:
                    abbreviation = flatten_list_2d(value['abbreviation'].values())
                    abbreviation_str = ", ".join(abbreviation)
                    value2str = ", ".join(value['enum'])
                    parameter_properties_to_string = f"### {key.upper()}: {value2str}, {abbreviation_str}"
                    parameter_info.append(parameter_properties_to_string)
        
        parameter_info_to_string = "\n".join(parameter_info)
        return parameter_info_to_string


    def __get_default_value(self, function_called: str) -> str:
        func_info = self.report_config[function_called]
        parameter_properties = func_info['function']['parameters']['properties']
        
        default_value = {}
        for key, value in parameter_properties.items():
            default_value[key] = value['default']
        return default_value
    
    
    def __get_abbreviation(self, function_called: str) -> str:
        func_info = self.report_config[function_called]
        properties = func_info['function']['parameters']['properties']
        
        abbreviation = []
        for key, value in properties.items():
            if "abbreviation" in value:
                subabbreviation = []
                
                abbreviation_dict = value['abbreviation']
                for product, abbr_list in abbreviation_dict.items():
                    abbreviation_str = ", ".join(abbr_list)
                    subabbreviation.append(f"- {product}: {abbreviation_str}")
                subabbreviation_str = "\n".join(subabbreviation)
                format_abbreviation = f"""
                #### {key}:
                {subabbreviation_str}
                """
                abbreviation.append(format_abbreviation)
                
        abbreviation_str = "\n".join(abbreviation)
        return abbreviation_str
    
    
    def extract_entities(self, query: str, function_called: str) -> Dict[str, Any]:
        """
        Process the input text and extract named entities using Ollama API.
        
        Args:
            query (str): The input query to process
            
        Returns:
            Dict[str, Any]: Dictionary containing extracted entities and their metadata
        """
        
        parameter_properties = self.__get_parameter_properties(function_called)
        # abbreviation = self.__get_abbreviation(function_called)
        agent = self.agent_config.get_agent(function_called)
        
        user_prompt = agent.format_prompt(
            query=query,
            parameter_properties=parameter_properties,
            # abbreviation=abbreviation
        )
        print(user_prompt)
        messages = [
            {"role": "system", "content": agent.system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = self.llm.invoke(
            messages=messages,
            format_schema=agent.format_schema,
            model=self.model,
            endpoint='/api/chat'
        )
        
        if not json.loads(response):
            return self.__get_default_value(function_called)
            
        return json.loads(response)