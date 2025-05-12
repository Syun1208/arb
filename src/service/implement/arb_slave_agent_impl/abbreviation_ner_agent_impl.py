from typing import Dict, Any, List
import json
from concurrent.futures import ThreadPoolExecutor

from src.service.interface.arb_slave_agent.ner_agent import NerAgent
from src.service.interface.arb_supporter.llm import LLM
from src.service.implement.arb_supporter_impl.prompt_impl import NerAgentConfig
from src.utils.utils import extract_number, flatten_list_2d


class AbbreviationNERAgentImpl(NerAgent):
    
    """
    Implementation of AbbreviationNERAgentImpl using Ollama API for Named Entity Recognition.
    """
    
    def __init__(
        self,
        llm: LLM,
        model: str, 
        name: str,
        task_description: str,
        report_config: Dict[str, Any],
        agent_config: NerAgentConfig,
        tools: List[Any],
        num_workers: int
    ) -> None:
        super(AbbreviationNERAgentImpl, self).__init__()
        
        self.llm = llm
        self.model = model
        self.name = name
        self.task_description = task_description
        self.report_config = report_config
        self.agent_config = agent_config()
        self.tools = tools
        self.num_workers = num_workers
        
        
    def __repr__(self) -> str:
        return f"{self.name}: {self.task_description}"
    

    def _get_default_value(self, function_called: str) -> str:
        func_info = self.report_config[function_called]
        parameter_properties = func_info['function']['parameters']['properties']
        
        default_value = {}
        for key, value in parameter_properties.items():
            default_value[key] = value['default']
            
        if function_called in ["/winlost_detail", "/turnover"]:
            default_value['date_range'] = "N/A"
            
        return default_value
    
    
    def __get_abbreviated_parameters(self, function_called: str) -> List[str]:
        parameter_properties = self.report_config[function_called]['function']['parameters']['properties']
        
        list_abbreviation_prompt = []
        for param, param_info in parameter_properties.items():
            
            if "abbreviation" in param_info:
                list_abbreviation_prompt = []
                for key, value in param_info['abbreviation'].items():
                    
                    prompt = f"""
                    {value} => {key}
                    """
                    list_abbreviation_prompt.append(prompt)
                list_abbreviation_prompt2text = f"{param}:\n" + "\n".join(list_abbreviation_prompt)
                list_abbreviation_prompt.append(list_abbreviation_prompt2text)
                
        return "\n".join(list_abbreviation_prompt)
    
    
    def __get_specific_info_parameters(self, function_called: str, name_parameter: str) -> List[str]:
        parameter_properties = self.report_config[function_called]['function']['parameters']['properties']
        param_info = parameter_properties[name_parameter]
        enum = param_info['enum']
        abbreviation_prompt2text = ""

            
        if "abbreviation" in param_info:
            list_abbreviation_prompt = []
            for key, value in param_info['abbreviation'].items():
                
                prompt = f"""
                {value} => {key}
                """
                list_abbreviation_prompt.append(prompt)
            abbreviation_prompt2text = f"{name_parameter}:\n" + "\n".join(list_abbreviation_prompt)
                
        return abbreviation_prompt2text, enum
    
    
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
    
    def __handle_username(self, function_called: str, entities: Dict[str, Any]) -> Dict[str, Any]:
        
        if len(entities['user'].split(" ")) > 1:
            entities['user'] = "N/A"
            return entities
        
        if function_called in ["/winlost_detail", "/turnover"]:
            parameter_properties = self.report_config[function_called]['function']['parameters']['properties']
            for _, value in parameter_properties.items():
                if "abbreviation" in value:
                    flattened_abbreviation = flatten_list_2d(value['abbreviation'].values())
                    lower_abbreviation = [abbreviation.lower() for abbreviation in flattened_abbreviation]
                    upper_abbreviation = [abbreviation.upper() for abbreviation in flattened_abbreviation]
                    capitalized_abbreviation = [abbreviation.capitalize() for abbreviation in flattened_abbreviation]
                    combined_abbreviation = flattened_abbreviation + lower_abbreviation + upper_abbreviation + capitalized_abbreviation
                    if entities['user'] in combined_abbreviation:
                        entities['user'] = "N/A"
        
        return entities

    def __call_llm_extracting(self, prompt: str, config: Any):
        response = self.llm.invoke(
            messages=[
                {"role": "system", "content": config.system_prompt},
                {"role": "user", "content": prompt}
            ],
            format_schema=config.format_schema,
            model=self.model,
            endpoint='/api/chat'
        )
        return json.loads(response)
    
    
    def extract_entities(self, query: str, function_called: str) -> Dict[str, Any]:
        """
        Process the input text and extract named entities using Ollama API.
        
        Args:
            query (str): The input query to process
            
        Returns:
            Dict[str, Any]: Dictionary containing extracted entities and their metadata
        """
        
        agent = self.agent_config.get_agent(function_called)

        if function_called in ["/winlost_detail", "/turnover"]:
            extracted_entities = {}

            # Prompts
            abbreviated_product_parameters, product_enum = self.__get_specific_info_parameters(function_called, "product")
            abbreviated_product_detail_parameters, product_detail_enum = self.__get_specific_info_parameters(function_called, "product_detail")
            abbreviated_level_parameters, level_enum = self.__get_specific_info_parameters(function_called, "level")
            
            date_range_prompt = agent.format_date_range_prompt(query=query)
            product_prompt = agent.format_product_prompt(
                query=query, 
                product_enum=product_enum,
                abbreviated_parameters=abbreviated_product_parameters
            )
            product_detail_prompt = agent.format_product_detail_prompt(
                query=query,
                product_detail_enum=product_detail_enum,
                abbreviated_parameters=abbreviated_product_detail_parameters
            )
            level_prompt = agent.format_level_prompt(
                query=query, 
                level_enum=level_enum,
                abbreviated_parameters=abbreviated_level_parameters
            )
            # remaining_parameters_prompt = agent.format_the_others_prompt(query=query, abbreviated_parameters=abbreviated_parameters)

            # Run extractions in parallel using threads
            with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
                date_range_future = executor.submit(self.__call_llm_extracting, date_range_prompt, agent.date_range_config)
                product_future = executor.submit(self.__call_llm_extracting, product_prompt, agent.product_config)
                product_detail_future = executor.submit(self.__call_llm_extracting, product_detail_prompt, agent.product_detail_config)
                level_future = executor.submit(self.__call_llm_extracting, level_prompt, agent.level_config)
                # remaining_params_future = executor.submit(self.__call_llm_extracting, remaining_parameters_prompt, agent.the_others_config)

                date_range_response = date_range_future.result()
                product_response = product_future.result()
                product_detail_response = product_detail_future.result()
                level_response = level_future.result()
                # remaining_parameters_response = remaining_params_future.result()

            # Update extracted entities with results
            extracted_entities.update(date_range_response)
            extracted_entities.update(product_response)
            extracted_entities.update(product_detail_response)
            extracted_entities.update(level_response)
            
            extracted_entities = self.__handle_username(function_called, extracted_entities)

        else:
            abbreviated_parameters = self.__get_abbreviated_parameters(function_called)
            user_prompt = agent.format_prompt(
                query=query,
                abbreviated_parameters=abbreviated_parameters
            )
            extracted_entities = self.__call_llm_extracting(user_prompt, agent)

            if not extracted_entities:
                return self._get_default_value(function_called)
            
            extracted_entities = self.__handle_result_topoutstanding(function_called, extracted_entities, query)
        
        extracted_entities = self.__validate(function_called, extracted_entities)
        return extracted_entities