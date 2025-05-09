import json
from typing import List, Dict, Any
import re

from src.service.interface.arb_supporter.llm import LLM
from src.service.interface.arb_slave_agent.ner_agent import NerAgent
from src.service.implement.arb_supporter_impl.prompt_impl import NerAgentConfig
from src.utils.utils import flatten_list_2d, get_last_week_dates, get_last_year_dates, get_last_month_dates, get_this_year_dates

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

        agent = self.agent_config.get_agent(function_called)
        # abbreviation = self.__get_abbreviation(function_called)
        if function_called in ["/winlost_detail", "/turnover"]:
            extracted_entities = {}

            # Extract date range
            date_range_prompt = agent.format_date_range_prompt(query=query, parameter_properties=parameter_properties)
            date_range_response = self.llm.invoke(
                messages=[
                    {"role": "system", "content": agent.date_range_config.system_prompt},
                    {"role": "user", "content": date_range_prompt}
                ],
                format_schema=agent.date_range_config.format_schema,
                model=self.model,
                endpoint='/api/chat'
            )
            print(f"Date range response: {date_range_response}")
            extracted_entities.update(json.loads(date_range_response))

            # Extract product
            product_enum = self.report_config[function_called]['function']['parameters']['properties']['product']['enum']
            product_prompt = agent.format_product_prompt(query, product_enum)
            product_response = self.llm.invoke(
                messages=[
                    {"role": "system", "content": agent.product_config.system_prompt},
                    {"role": "user", "content": product_prompt}
                ],
                format_schema=agent.product_config.format_schema,
                model=self.model,
                endpoint='/api/chat'
            )
            product_data = json.loads(product_response)
            extracted_product = product_data.get("product", "All")
            if extracted_product != "All":
                product_candidates = [p.strip() for p in extracted_product.split(',')]
                # product_case_map = {p.lower(): p for p in product_enum}
                valid_products = [p for p in product_candidates if p in product_enum]
                extracted_entities["product"] = ", ".join(valid_products) if valid_products else "All"
            else:
                extracted_entities["product"] = "All"

            # Extract product detail
            product_detail_enum = self.report_config[function_called]['function']['parameters']['properties']['product_detail']['enum']
            product_detail_prompt = agent.format_product_detail_prompt(query, product_detail_enum)
            product_detail_response = self.llm.invoke(
                messages=[
                    {"role": "system", "content": agent.product_detail_config.system_prompt},
                    {"role": "user", "content": product_detail_prompt}
                ],
                format_schema=agent.product_detail_config.format_schema,
                model=self.model,
                endpoint='/api/chat'
            )
            product_detail_data = json.loads(product_detail_response)
            extracted_product_detail = product_detail_data.get("product_detail", "All")
            if extracted_product_detail != "All":
                product_detail_candidates = [p.strip() for p in extracted_product_detail.split(',')]
                # product_detail_case_map = {p.lower(): p for p in product_detail_enum}
                valid_product_details = [p for p in product_detail_candidates if p in product_detail_enum]
                extracted_entities["product_detail"] = ", ".join(valid_product_details) if valid_product_details else "All"
            else:
                extracted_entities["product_detail"] = "All"

            # Extract level
            level_enum = self.report_config[function_called]['function']['parameters']['properties']['level']['enum']
            level_prompt = agent.format_level_prompt(query, level_enum)
            level_response = self.llm.invoke(
                messages=[
                    {"role": "system", "content": agent.level_config.system_prompt},
                    {"role": "user", "content": level_prompt}
                ],
                format_schema=agent.level_config.format_schema,
                model=self.model,
                endpoint='/api/chat'
            )
            print(f"Level response: {level_response}")
            level_data = json.loads(level_response)
            extracted_level = level_data.get("level", "All")
            if extracted_level != "All":
                level_candidates = [p.strip() for p in extracted_level.split(',')]
                # level_case_map = {p.lower(): p for p in level_enum}
                valid_levels = [p for p in level_candidates if p in level_enum]
                extracted_entities["level"] = ", ".join(valid_levels) if valid_levels else "All"
            else:
                extracted_entities["level"] = "All"


            # Return all extracted entities
            return extracted_entities
        
        
        else:
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
        
            return result
