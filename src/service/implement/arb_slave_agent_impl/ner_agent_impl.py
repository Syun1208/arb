import json
from typing import List, Dict, Any
import re

from src.service.interface.arb_supporter.llm import LLM
from src.service.interface.arb_slave_agent.ner_agent import NerAgent
from src.service.implement.arb_supporter_impl.prompt_impl import NerAgentConfig
from src.utils.utils import flatten_list_2d, parse_2d_to_2key_2value, switch_key_value, extract_number, filter_words

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
                    # abbreviation = flatten_list_2d(value['abbreviation'].values())
                    # abbreviation_str = ", ".join(abbreviation)
                    value2str = ", ".join(value['enum'])
                    parameter_properties_to_string = f"### {key.upper()}: {value2str}"
                    parameter_info.append(parameter_properties_to_string)
        
        parameter_info_to_string = "\n".join(parameter_info)
        return parameter_info_to_string


    def _get_default_value(self, function_called: str) -> str:
        func_info = self.report_config[function_called]
        parameter_properties = func_info['function']['parameters']['properties']
        
        default_value = {}
        for key, value in parameter_properties.items():
            default_value[key] = value['default']
            
        if function_called in ["/winlost_detail", "/turnover"]:
            default_value['date_range'] = "N/A"
            
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
                    abbr_list = ", ".join(abbr_list)
                    subabbreviation.append(f"{abbr_list}")
                subabbreviation_str = ", ".join(subabbreviation)
                format_abbreviation = f"""
                ### {key.upper()}: {subabbreviation_str}
                """
                abbreviation.append(format_abbreviation)
                
        abbreviation_str = "\n".join(abbreviation)
        return abbreviation_str

    
    def __map_abbreviation(self, function_called: str, entities: Dict[str, Any]) -> Dict[str, Any]:
        func_info = self.report_config[function_called]
        properties = func_info['function']['parameters']['properties']
        
        for key, value in properties.items():

            if "abbreviation" in value:
                parse_abbreviation = parse_2d_to_2key_2value(value['abbreviation'])
                parse_abbreviation = switch_key_value(parse_abbreviation)
                if entities[key] in parse_abbreviation.keys():
                    entities[key] = parse_abbreviation[entities[key]]

        return entities
    
    
    def __validate(self, function_called: str, entities: Dict[str, Any]) -> bool:

        func_info = self.report_config[function_called]
        parameter_properties = func_info['function']['parameters']['properties']

        for key, value in parameter_properties.items():
            if value['enum'] is not None:
                if entities[key] not in value['enum']:
                    entities[key] = value['default']
                
        return entities
    
    
    def __handle_result_topoutstanding(self, function_called: str, entities: Dict[str, Any], query: str) -> Dict[str, Any]:
    
        if function_called == "/topoutstanding":
            top = extract_number(query)
            default_value = self._get_default_value(function_called)
            if entities['top'] == default_value['top'] and top is not None:
                entities['top'] = top
        
        return entities
    
    
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
            return self._get_default_value(function_called)
        
        result = json.loads(response)
        result = self.__validate(function_called, result)
        result = self.__handle_result_topoutstanding(function_called, result, query)
        
        return result
