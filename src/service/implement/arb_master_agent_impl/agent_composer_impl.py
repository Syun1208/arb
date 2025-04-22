from typing import Dict, Any, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor

from src.model.alpha_metadata import AlphaMetadata, Params
from src.model.alpha_status_code import AlphaStatusCode
from src.service.interface.arb_master_agent.agent_composer import AgentComposer
from src.service.interface.arb_slave_agent.recognizer_agent import RecognizerAgent
from src.service.interface.arb_slave_agent.ner_agent import NerAgent
from src.service.interface.arb_slave_agent.report_calling_agent import ReportCallingAgent
from src.service.interface.arb_slave_agent.greeting_agent import GreetingAgent
from src.service.interface.arb_service.arb_db_service import ARBDBService
from src.utils.utils import format_entities_for_prompt
from src.utils.constants import FUNCTION_MAPPING_NAME

class AgentComposerImpl(AgentComposer):
    """
    Implementation of AgentComposer for the Predator chatbot system.
    This class manages multiple AI agents and their interactions for the Predator chatbot.
    """

    def __init__(
        self,
        greeting_agent: GreetingAgent,
        confirmation_recognizer_agent: RecognizerAgent,
        ner_agent: NerAgent,
        report_calling_agent: ReportCallingAgent,
        greeting_recognizer_agent: RecognizerAgent,
        database: ARBDBService,
        num_workers: int
    ) -> None:
        """
        Initialize the AgentComposer with required agents and configuration.

        Args:
            greeting_agent: GreetingAgent
            confirmation_recognizer_agent: RecognizerAgent
            ner_agent: NerAgent
            report_calling_agent: ReportCallingAgent
            greeting_recognizer_agent: RecognizerAgent
            database: ARBDBService
            num_workers: int
        """
        # Initialize the agents
        self.greeting_agent = greeting_agent
        self.confirmation_recognizer_agent = confirmation_recognizer_agent
        self.ner_agent = ner_agent
        self.database = database
        self.report_calling_agent = report_calling_agent
        self.greeting_recognizer_agent = greeting_recognizer_agent
        self.num_workers = num_workers

        
    @staticmethod
    def __update_entities(previous_params: Dict[str, str], current_params: Dict[str, str]) -> Dict[str, str]:
        """
        Update the params from the from_params to the to_params
        Args:
            previous_params: The previous params
            current_params: The current params
        Returns:
            The updated params
        """
        if not previous_params:
            return current_params
        
        del current_params['date_range']
        updated_params = current_params.copy()
        
        if current_params['from_date'] != 'N/A':
            updated_params['from_date'] = current_params['from_date']
            
        if current_params['to_date'] != 'N/A':
            updated_params['to_date'] = current_params['to_date']
        
        for key, value in updated_params.items():
            if value == "N/A" or value == 'All':
                updated_params[key] = previous_params[key]
        return updated_params

    def __format_date(self, date: str) -> str:
        """
        Format the date to YYYY-MM-DD
        Args:
            date: The date to format
        Returns:
            The formatted date
        """
        date_info = date.split('-')
        day = date_info[0]
        month = date_info[1]
        year = date_info[2]
        if len(year) == 4:
            return f"{year}-{month}-{day}"
        return date

    def __run_agent(self, agent: Any, method: str, arg: str) -> Any:
        """
        Run the agent with the method and argument
        """
        return getattr(agent, method)(arg)
    
    def __get_status_code(self, params: Optional[Dict[str, str]], endpoint: Optional[str]) -> AlphaStatusCode:
        """
        Get the status code
        """
        # First check if params or endpoint is None
        if params is None and endpoint is None:
            return AlphaStatusCode(status_code=414, message="Do not provide any params and function/report")
            
        if params is None:
            return AlphaStatusCode(status_code=410, message="Do not provide any params")
        
        if endpoint is None:
            return AlphaStatusCode(status_code=411, message="Could not find any function/report")
        
        # Then check date range validity
        if params['from_date'] == 'N/A' and params['to_date'] == 'N/A':
            return AlphaStatusCode(status_code=412, message="Do not provide any date range (required)")
        
        if params['from_date'] == 'N/A' and params['to_date'] != 'N/A':
            return AlphaStatusCode(status_code=413, message="From date is required when to date is provided")
        
        return AlphaStatusCode(status_code=209, message="Confirmation is accepted")

    async def compose(self, user_id: str, message: str) -> Tuple[AlphaMetadata, AlphaStatusCode]:
        """
        Process a message through the multi-agent system.

        Args:
            user_id: The user ID to process
            message: The input message to process

        Returns:
            str: The response generated by the agent system
        """
        
        # Initialize the flags
        is_new_session = False
        is_action = False
        alpha_status_code = None
        alpha_status_code = AlphaStatusCode(status_code=200, message="Success")
        
        is_normal_conversation = self.greeting_recognizer_agent.get_decision(message)
        is_confirmed = self.confirmation_recognizer_agent.get_decision(message)
        if is_confirmed:
            is_normal_conversation = False
        
        if not is_normal_conversation:
            # Run agents in parallel using thread pool
            with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
                # Submit all tasks
                entity_future = executor.submit(self.__run_agent, self.ner_agent, 'extract_entities', message)
                function_future = executor.submit(self.__run_agent, self.report_calling_agent, 'call_report', message)
                
                # Get results as they complete
                entities = entity_future.result()
                function_called = function_future.result()
            
            
            # Convert endpoint to None if it is N/A
            if function_called == "N/A":
                function_called = None
            print('🤖 function_called: ', function_called)

            
            # Get the latest function
            previous_function = None
            previous_params = {}
            if self.database.get(user_id):
                user_database = self.database.get(user_id)
                previous_function = user_database[-1]['endpoint']
                previous_params = user_database[-1]['params']
            
            # Update the params
            update_entities = self.__update_entities(previous_params, entities)


            # Case 1: is_action            
            if is_confirmed:
                is_action = True
            print('🤖 is_action: ', is_action)
            # Case 2: is_new_session
            
            # Save the function called
            if function_called is None and previous_function is not None:
                function_called = previous_function
            print('🤖 previous_function: ', previous_function)
            print('🤖 function_called updated: ', function_called)
            function_name = FUNCTION_MAPPING_NAME[function_called]
            
            # Define the normal conversation
            if is_action:
                is_normal_conversation = False
                alpha_status_code = self.__get_status_code(update_entities, function_called)
                
            print('🤖 is_normal_conversation: ', is_normal_conversation)
            
            # Case update function when the query is the greeting conversation
            if previous_function != function_called and previous_function is not None:
                is_new_session = True
                self.database.update(
                    user_id=user_id, 
                    metadata=[]
                )
            
            if not is_new_session:
                entities = update_entities
                
            # Generate response based on tasks, entities and confirmation
            # Check if date range is specified
            message_non_date = ""
            if entities['from_date'] == 'N/A':
                message_non_date = "❌ Please specify the date range for your request to proceed with generating the report."

            # Build base response with parameters
            base_params = f"""
📅 Date Range: {entities['from_date']} - {entities['to_date']}
🏢 Product: {entities['product']} 
📋 Product Detail: {entities['product_detail']}
🎮 Level: {entities['level']}
👤 Username: {entities['user']}"""

            # Handle action case
            if is_action:
                if entities['from_date'] == 'N/A':
                    response = f"""
⚠️ NOTE THAT: 
    📅 From Date: REQUIRED
    📅 To Date: REQUIRED
    🏢 Product: Default is All
    📋 Product Detail: Default is All
    🎮 Level: Default is All
    👤 User: Default is N/A
    
✅YOUR CURRENT PARAMETERS:
{base_params}
    
{message_non_date}"""
                else:
                    response = f"""{base_params}

✅ Your request has been confirmed, please wait for a moment to get the report."""

            # Handle non-action case
            else:
                response = f"""{base_params}
        
⚠️ Would you like to confirm this information and proceed with the report generation?
{message_non_date}"""

            # Add header based on function status
            if function_called is None:
                header = "🎲 Here is the summary of parameters:"
                function_warning = """
⚠️ NOTE THAT: You should not confirm the information if you have not specified the function to proceed with generating the report.
❌ Could not find the Function/Report. Please specify the function to proceed with generating the report."""
                response = f"{header}\n{response}\n{function_warning}"
            
            else:
                header = f"🎲 Here is the summary of parameters for {function_name}:"
                response = f"{header}\n{response}"
                
            print(f'🕵️ Request: {message}\n')
            print(f'🤖 Response: {response}\n') 
                
            print('🤖 current_params: \n', format_entities_for_prompt(entities))
            print('🤖 previous_params: \n', format_entities_for_prompt(previous_params))
                
            print("🩻 is_new_session: ", is_new_session)
            # Create params
            params = Params(
                from_date=entities['from_date'],
                to_date=entities['to_date'],
                product=entities['product'],
                product_detail=entities['product_detail'],
                level=entities['level'],
                user=entities['user']
            )
            
            # Update the metadata
            alpha_metadata = AlphaMetadata(
                user_id=user_id,
                is_new_session=is_new_session,
                is_action=is_action,
                endpoint=function_called,
                params=params,
                response=response
            )
            
            # BUG: Format date to YYYY-MM-DD
            if alpha_metadata.params.from_date != "N/A":
                alpha_metadata.params.from_date = alpha_metadata.params.from_date.replace("/", "-") 
                alpha_metadata.params.from_date = self.__format_date(alpha_metadata.params.from_date)
                alpha_metadata.params.to_date = alpha_metadata.params.to_date.replace("/", "-")
                alpha_metadata.params.to_date = self.__format_date(alpha_metadata.params.to_date)
            
            
            print("👻 Params insert into database: \n")
            print(format_entities_for_prompt(alpha_metadata.to_dict()))
            
            # Insert the metadata into the database
            metadata_chain = self.database.get(user_id)
            if metadata_chain:
                metadata_chain.append(alpha_metadata.to_dict())
                self.database.insert(
                    user_id=user_id,
                    metadata=metadata_chain
                )
            else:
                self.database.insert(
                    user_id=user_id,
                    metadata=[alpha_metadata.to_dict()]
                )
                
            # Convert field user to None if it is N/A
            if alpha_metadata.params.user == "N/A":
                alpha_metadata.params.user = None
            
            # Convert params to None if from_date or function_called is N/A
            if not is_action:
                alpha_metadata.params = None
                alpha_metadata.endpoint = None
            
            if is_action and alpha_metadata.params.from_date == 'N/A':
                alpha_metadata.params = None
                alpha_metadata.endpoint = None
                
            print("👻 Params show for user: \n")
            print(format_entities_for_prompt(alpha_metadata.to_dict()))
        
        else:
            response = self.greeting_agent.chat(message)
            alpha_metadata = AlphaMetadata(
                user_id=user_id,
                is_new_session=False,
                is_action=False,
                endpoint=None,
                params=None,
                response=response
            )
            alpha_status_code = AlphaStatusCode(status_code=104, message="Casual conversation")
            
        return alpha_metadata, alpha_status_code
