import json
from typing import Dict, Any, List

from src.service.interface.arb_slave_agent.report_calling_agent import ReportCallingAgent
from src.utils.constants import ReportCallingAgentConfig
from src.service.interface.arb_supporter.llm import LLM

class ReportCallingAgentImpl(ReportCallingAgent):
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
        Initialize the ReportCallingAgentImpl with the given LLM, name, task description, agent configuration, report configuration, and tools.
        
        Args:
            llm (LLM): The LLM instance
            model (str): The model to use
            name (str): The name of the agent
            task_description (str): The description of the task
            report_config (Dict[str, Any]): The configuration for the report
            tools (List[Any]): The tools available to the agent
        """
        super(ReportCallingAgentImpl, self).__init__()
        
        self.llm = llm
        self.model = model
        self.name = name
        self.task_description = task_description
        self.agent_config = ReportCallingAgentConfig()
        self.format_schema = self.agent_config.format_schema
        self.system_prompt = self.agent_config.system_prompt
        self.user_prompt = self.agent_config.user_prompt
        self.instruction = self.agent_config.instruction
        self.few_shot = self.agent_config.few_shot
        self.report_config = report_config
        self.tools = tools


    def __repr__(self) -> str:
        return f"{self.name}: {self.task_description}"


    def __get_abbreviation(self) -> str:
        
        abbreviated_functions = []
        for func_info in self.report_config:
            abbreviation = func_info['abbreviation']
            function_name = func_info['name']
            format_schema = f"- {abbreviation}: {function_name}"
            abbreviated_functions.append(format_schema)
        
        abbreviated_functions_to_string = "\n".join(abbreviated_functions)
        return abbreviated_functions_to_string
    
    
    def __get_function_description(self) -> str:
        function_descriptions = []
        for func_info in self.report_config:
            function_description = func_info['description']
            function_descriptions.append(function_description)
        function_descriptions_to_string = "\n".join(function_descriptions)
        return function_descriptions_to_string


    def call_report(self, message: str) -> Dict[str, Any]:
        
        abbreviation = self.__get_abbreviation()
        function_description = self.__get_function_description()
    
        user_prompt = self.user_prompt.format(
            query=message, 
            instruction=self.instruction.format(
                abbreviation=abbreviation,
                function_description=function_description
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
        
        if 'function_called' in json.loads(response):
            return json.loads(response)['function_called']
        
        return 'N/A'