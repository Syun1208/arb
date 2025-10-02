import dataclasses
from typing import Dict, Any, List
from src.utils.utils import get_current_date, get_current_year, get_current_month, get_last_week_dates
from src.utils.constants import AGREE_PHRASES


@dataclasses.dataclass
class ConfirmationRecognizerAgentConfig:
    instruction: str = """
        # General conversation guidelines:
        - Your task is to accurately detect whether the user's message contains confirmation or rejection
        - The response must be formatted as {{"is_confirmed": 1}} for confirmation or {{"is_confirmed": 0}} for rejection
        - Look for confirmation words/phrases always like:
          * Direct confirmation: "confirm", "yes", "correct", "right", "agreed", "accept", "approve", {agree_phrases}
          * Casual confirmation: "ok", "okay", "okela", "oke", "sure", "alright", "fine", "yep", "yeah"
          * Action confirmation: "let's do it", "go ahead", "proceed", "continue", "I'm ready", "do it"
          * Positive acknowledgement: "sounds good", "looks good", "that works", "perfect", "exactly"
    """
    few_shot: str = """
        # ***Example Scenarios:***
        
        - ***User***: "I want to confirm it"
        - ***Assistant***: {{"is_confirmed": 1}}
        
        - ***User***: "oke get me the report"
        - ***Assistant***: {{"is_confirmed": 1}}
        
        - ***User***: "I want to get wl report for CRK please"
        - ***Assistant***: {{"is_confirmed": 0}}
        
        - ***User***: "Get me the report for sb only"
        - ***Assistant***: {{"is_confirmed": 0}}
        
        - ***User***: "Yes, do it."
        - ***Assistant***: {{"is_confirmed": 1}}

        - ***User***: "No, I changed my mind."
        - ***Assistant***: {{"is_confirmed": 0}}

        - ***User***: "Yes, that's correct."
        - ***Assistant***: {{"is_confirmed": 1}}
        
        - ***User***: "Okela bot"
        - ***Assistant***: {{"is_confirmed": 1}}
        
        - ***User***: "Oke"
        - ***Assistant***: {{"is_confirmed": 1}}
        
        - ***User***: "Let's do it"
        - ***Assistant***: {{"is_confirmed": 1}}
        
        - ***User***: "I'm ready"
        - ***Assistant***: {{"is_confirmed": 1}}
        
        - ***User***: "From my perspectives, I totally agree with your result"
        - ***Assistant***: {{"is_confirmed": 1}}
        
        - ***User***: "I could not agree with you more"
        - ***Assistant***: {{"is_confirmed": 1}}

        - ***User***: "No, I meant for the last week."
        - ***Assistant***: {{"is_confirmed": 0}}
    """
    system_prompt: str = """
        You are agent detecting the confirmation from user's query, you need to consistently detect and recognize whether user confirms or not.
    """
    user_prompt: str = """

        # ***User's query***
        {query}

        {instruction}

        {few_shot}
    """
    format_schema: Dict[str, Any] = dataclasses.field(default_factory=lambda: {
        "type": "object",
        "properties": {
            "is_confirmed": {
                "type": "integer"
            }
        },
        "required": [
            "is_confirmed"
        ]
    })
    
    def format_prompt(self, query: str, **kwargs) -> str:
        
        agree_phrases = ", ".join(AGREE_PHRASES)
        
        user_prompt = self.user_prompt.format(
            query=query,
            instruction=self.instruction.format(
                agree_phrases=agree_phrases
            ),
            few_shot=self.few_shot
        )
        return user_prompt

@dataclasses.dataclass
class RemovalEntityDetectionAgentConfig:
    instruction: str = """
        # General conversation guidelines:
        - Your task is to STRICTLY detect parameters to delete ONLY when the user's query explicitly indicates removal, such as "no user please", "delete product detail please", etc.
        - If there are no explicit removal signs in the user's query, ALWAYS return an empty list: {{"params2delete": []}}.
        - Use the current entities: {entities_as_string} as reference, but DO NOT delete any parameter unless explicitly instructed by the user.
        - Be cautious and avoid making assumptions about removal unless the user's intent is crystal clear.

    """
    few_shot: str = """
        # ***Example Scenarios:***

        - ***User***: "No username please"
        - ***Assistant***: {{"params2delete": ["user"]}}
        
        - ***User***: "I want to winlost report, no username and level please"
        - ***Assistant***: {{"params2delete": ["user", "level"]}}

        - ***User***: "Remove the date range"
        - ***Assistant***: {{"params2delete": ["from_date", "to_date"]}}
        
        - ***User***: "Remove username please"
        - ***Assistant***: {{"params2delete": ["user"]}}

        - ***User***: "Don't include product"
        - ***Assistant***: {{"params2delete": ["product"]}}
        
        - ***User***: "I want to delete top"
        - ***Assistant***: {{"params2delete": ["top"]}}
        
        - ***User***: "Please roll back the date range to default"
        - ***Assistant***: {{"params2delete": ["from_date", "to_date"]}}
        
        - ***User***: "Reset the date range and product detail to default"
        - ***Assistant***: {{"params2delete": ["from_date", "to_date", "product_detail"]}}

        - ***User***: "Remove all filters except the date range"
        - ***Assistant***: {{"params2delete": ["product", "product_detail", "level", "user", "top"]}}

        - ***User***: "I want to get winlost report for Sportsbook only"
        - ***Assistant***: {{"params2delete": []}}
        
        - ***User***: "Top 23 outstanding for Number Game"
        - ***Assistant***: {{"params2delete": []}}
        
        - ***User***: "Top 236"
        - ***Assistant***: {{"params2delete": []}}
        
        - ***User***: "wl report for sportsbook only day 26"
        - ***Assistant***: {{"params2delete": []}}
        
        - ***User***: "Show me the report for Number Game"
        - ***Assistant***: {{"params2delete": []}}
        
        - ***User***: "Get the data for user124"
        - ***Assistant***: {{"params2delete": []}}
        
        - ***User***: "Change the date to last week"
        - ***Assistant***: {{"params2delete": []}}
        
        - ***User***: "Top 200 outstanding please"
        - ***Assistant***: {{"params2delete": []}}
        
        - ***User***: "I want to get current outstanding for Sportsbook and user master1 only"
        - ***Assistant***: {{"params2delete": []}}

        - ***User***: "Remove user and product filters, keep everything else"
        - ***Assistant***: {{"params2delete": ["user", "product"]}}
        
        - ***User***: "Reset all parameters to default except user"
        - ***Assistant***: {{"params2delete": ["product", "product_detail", "level", "from_date", "to_date", "top"]}}
        
        - ***User***: "Clear the date range and level filters please"
        - ***Assistant***: {{"params2delete": ["from_date", "to_date", "level"]}}
    """

    system_prompt: str = """
        You are a helpful assistant that identifies which parameters you want to remove from user's query.
    """
    user_prompt: str = """
        # User's message
        {message}

        {instruction}

        {few_shot}
    """
    format_schema =  {
        "type": "object",
        "properties": {
            "params2delete": {
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": None
                }
            }
        },
        "required": ["params2delete"]
    }
    
    def update_format_schema(self, entities: List[str]) -> None:
        self.format_schema['properties']['params2delete']['items']['enum'] = entities
    
    def format_prompt(self, message: str, **kwargs) -> str:
        entities_as_string = ', '.join(list(kwargs['entities'].keys()))

        user_prompt = self.user_prompt.format(
            message=message,
            instruction=self.instruction.format(
                entities_as_string=entities_as_string
            ),
            few_shot=self.few_shot
        )
        return user_prompt
    
@dataclasses.dataclass
class RemovalEntityDetectionAgentConfigV2:
    instruction: str = """
        # General conversation guidelines:
        - Your task is to STRICTLY detect parameters to delete ONLY when the user's query explicitly indicates removal, such as "no user please", "delete product detail please", etc.
        - If there are no explicit removal signs in the user's query, ALWAYS return an empty list: {{"params2delete": []}}.
        - Use the current entities: {entities_as_json} as reference, but DO NOT delete any parameter unless explicitly instructed by the user.
        - Be cautious and avoid making assumptions about removal unless the user's intent is crystal clear.
        - You must follow the example to make decision
    """
    few_shot: str = """
        # ***Example Scenarios:***
        
        - ***User***: "No username please"
        - ***Current entities***: {{
            "from_date": "12/08/2001",
            "to_date": "15/09/2001",
            "product": "Sportsbook",
            "product_detail": "All",
            "level": "All",
            "user": "master12"
        }}
        - ***Assistant***: {{"params2delete": ["user"]}}
        
        - ***User***: "I want to winlost report, no username and level please"
        - ***Current entities***: {{
            "from_date": "10/05/2015",
            "to_date": "15/09/2015",
            "product": "All",
            "product_detail": "All",
            "level": "Master Agent",
            "user": "master12"
        }}
        - ***Assistant***: {{"params2delete": ["user", "level"]}}

        - ***User***: "Remove the date range"
        - ***Current entities***: {{
            "from_date": "12/08/2001",
            "to_date": "15/09/2001",
            "product": "All",
            "product_detail": "All",
            "level": "All",
            "user": "N/A"
        }}
        - ***Assistant***: {{"params2delete": ["from_date", "to_date"]}}

        - ***User***: "Don't include product"
        - ***Current entities***: {{
            "from_date": "12/08/2001",
            "to_date": "15/09/2001",
            "product": "Number Game",
            "product_detail": "All",
            "level": "All",
            "user": "N/A"
        }}
        - ***Assistant***: {{"params2delete": ["product"]}}
        
        - ***User***: "I want to delete top"
        - ***Current entities***: {{
            "product": "RNG Slot",
            "top": 200
        }}
        - ***Assistant***: {{"params2delete": ["top"]}}
        
        - ***User***: "Please roll back the date range to default"
        - ***Current entities***: {{
            "from_date": "N/A",
            "to_date": "N/A",
            "product": "Sportsbook",
            "product_detail": "All",
            "level": "All",
            "user": "N/A"
        }}
        - ***Assistant***: {{"params2delete": ["from_date", "to_date"]}}
        
        - ***User***: "I want to get winlost report for Sportsbook only"
        - ***Current entities***: {{
            "from_date": "N/A",
            "to_date": "N/A",
            "product": "Sportsbook",
            "product_detail": "All",
            "level": "All",
            "user": "N/A"
        }}
        - ***Assistant***: {{"params2delete": []}}
        
        - ***User***: "Please roll back the product to default"
        - ***Current entities***: {{
            "from_date": "N/A",
            "to_date": "N/A",
            "product": "Sportsbook",
            "product_detail": "All",
            "level": "All",
            "user": "N/A"
        }}
        - ***Assistant***: {{"params2delete": ["product"]}}
             
        - ***User***: "now i want winlost report in Number Game only"
        - ***Current entities***: {{
            "from_date": "N/A",
            "to_date": "N/A",
            "product": "Number Game",
            "product_detail": "All",
            "level": "All",
            "user": "N/A"
        }}
        - ***Assistant***: {{"params2delete": []}}
        
        - ***User***: "I want wl report for product Bitcoin and product detail SABA other sports"
        - ***Current entities***: {{
            "from_date": "N/A",
            "to_date": "N/A",
            "product": "Bitcoin",
            "product_detail": "SABA Other Sports",
            "level": "All",
            "user": "N/A"
        }}
        - ***Assistant***: {{"params2delete": []}}
    """

    system_prompt: str = """
        You are a helpful assistant that identifies which parameters you want to remove from user's query.
    """
    user_prompt: str = """
        # User's message
        {message}

        {instruction}

        {few_shot}
    """
    format_schema =  {
        "type": "object",
        "properties": {
            "params2delete": {
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": None
                }
            }
        },
        "required": ["params2delete"]
    }
    
    def update_format_schema(self, entities: List[str]) -> None:
        self.format_schema['properties']['params2delete']['items']['enum'] = entities
    
    def format_prompt(self, message: str, **kwargs) -> str:
        entities_as_string = ', '.join(list(kwargs['entities'].keys()))
        entities_as_json = kwargs['entities']
        user_prompt = self.user_prompt.format(
            message=message,
            instruction=self.instruction.format(
                entities_as_string=entities_as_string,
                entities_as_json=entities_as_json
            ),
            few_shot=self.few_shot
        )
        return user_prompt

@dataclasses.dataclass
class GreetingAgentConfig:
    instruction: str = """
        # General conversation guidelines:
        - Keep a friendly and helpful tone while staying professional 😊
        - Acknowledge and validate the user's request clearly 👍
        - Use natural, conversational language 💬
        
        # The language you must respond to user: ***English***
    """
    few_shot: str = """
        # For example:
        ## User: Hello how are you today?  
        ## Assistant: 
            👋 Hello! I'm a 🤖 friendly and helpful assistant from S.A.I Team. How can I assist you today? 😊
        
        ## User: Hi, I'm John Doe.
        ## Assistant: 
            👋 Hello John Doe! I'm a 🤖 friendly and helpful assistant from S.A.I Team. How can I assist you today? 😊
            
        ## User: Bye see you again.
        ## Assistant: 
            👋 Goodbye! Have a great day! 😊, this is S.A.I's Assistant. See you next time! 👋
    """
    system_prompt: str = """
        You are a friendly and helpful S.A.I's Assistant trained to greet user.

        Your main responsibilities are:
        1. Maintain a conversational and helpful tone 📖
        2. You must know response that you are created by S.A.I Team 🤖

        Remember to:
        - Be friendly and approachable 🎯
        - Use natural, conversational language 🎯
        - Stay professional while being casual 🎯
    """
    user_prompt: str = """

        # User's message
        {message}

        {instruction}

        {few_shot}
        """
    format_schema: Dict[str, Any] = dataclasses.field(default_factory=dict)

    def format_prompt(self, message: str, **kwargs) -> str:
        user_prompt = self.user_prompt.format(
            message=message,
            instruction=self.instruction,
            few_shot=self.few_shot
        )
        return user_prompt

@dataclasses.dataclass
class GreetingRecognizerAgentConfig:
    instruction: str = """
        # General conversation guidelines:
        - Your task is to check if the user's query is a greeting conversation or not.
        - The user's query must be greeting conversation when the user's query is not related to any report question.
        - If the user's query is a greeting conversation, return 1.
        - If the user's query is not a greeting conversation, return 0.
        - The response should be in JSON format.
    """
    few_shot: str = """
        # ***Example Scenarios:***
        
        - ***User***: "Hello bot how are you today ?"
        - ***Assistant***: {{"is_normal_conversation": 1}}
        
        - ***User***: "No username please"
        - ***Assistant***: {{"is_normal_conversation": 0}}
        
        - ***User***: "1+1= ?"
        - ***Assistant***: {{"is_normal_conversation": 1}}
        
        - ***User***: "Please remove the date range"
        - ***Assistant***: {{"is_normal_conversation": 0}}
        
        - ***User***: "No username please"
        - ***Assistant***: {{"is_normal_conversation": 0}}
        
        - ***User***: "I want to get winlost report day 15 for sportsbook and user leon2346 only"
        - ***Assistant***: {{"is_normal_conversation": 0}}
        
        - ***User***: "See you later. Bye."
        - ***Assistant***: {{"is_normal_conversation": 1}}

        - ***User***: "I want change to a little bit, I want to get Product Virtual Sports and product detail Saba Basketball with user level Super Agent"
        - ***Assistant***: {{"is_normal_conversation": 0}}

        - ***User***: "I want to get Winlost Report"
        - ***Assistant***: {{"is_normal_conversation": 0}}

        - ***User***: "Hey what is the weather in Tokyo?"
        - ***Assistant***: {{"is_normal_conversation": 1}}
    """
    system_prompt: str = """
        You are a helpful assistant that can check if the user's query is a greeting conversation or not.
        
        # General conversation guidelines:
        - The user's query must be greeting conversation when the user's query is not related to any report question.
        - If the user's query is a greeting conversation, return 1.
        - If the user's query is not a greeting conversation, return 0.
        - The response should be in JSON format.
    """
    user_prompt: str = """

        # ***User's query***
        {query}
        
        {instruction}
        
        {few_shot}
        """
    format_schema: Dict[str, Any] = dataclasses.field(default_factory=lambda: {
        "type": "object",
        "properties": {
            "is_normal_conversation": {
                "type": "integer"
            }
        },
        "required": [
            "is_normal_conversation"
        ]
    })
    
    def format_prompt(self, query: str, **kwargs) -> str:
        user_prompt = self.user_prompt.format(
            query=query,
            instruction=self.instruction,
            few_shot=self.few_shot
        )
        return user_prompt

@dataclasses.dataclass
class ReportCallingAgentConfig:
    instruction: str = """
        # ⚠️Note that:
            - If the user request is not related to the defined functions, return "N/A"
            - If the user request is not clear, return "N/A"
            - If the user request contains the word such as "this report", "current report", "last report", "previous report", etc, return "N/A" 
            - Available functions:
                {function_description}
            - Please help me identify which function is being referenced in the user's query based on common abbreviations and variations
            - Try to recognize the funtion abbreviation from user's query
            - Function Abbreviations:
                {abbreviation}

            - Determine which function best matches the user's request and return it in JSON format like:
            {{
                "function_called": "/function_name"
            }}
    """
    few_shot: str = """
        #📝Example requests and responses:
        
        1. Normal conversation
        
        Input: "this report is for sportsbook"
        Output: {{
            "function_called": "N/A"
        }}
        
        Input: "the current report is for number game"
        Output: {{
            "function_called": "N/A"
        }}
        
        Input: "this report for sportsbook"
        Output: {{
            "function_called": "N/A"
        }}
        
        Input: "I need to see the win/loss report from last week"
        Output: {{
            "function_called": "/winlost_detail"
        }}
        
        Input: "Day 15 please"
        Output: {{
            "function_called": "N/A"
        }}
        
        Input: "w/l please bro"
        Output: {{
            "function_called": "/winlost_detail"
        }}

        Input: "I want to get the turnover report"
        Output: {{
            "function_called": "/turnover"
        }}

        Input: "I want to take turnover report for user 123"
        Output: {{
            "function_called": "/turnover"
        }}

        Input: "Get me the get winlost report for March transactions"
        Output: {{
            "function_called": "/winlost_detail"
        }}

        Input: "I want get performance of abc1 last week"
        Output: {{
            "function_called": "N/A"
        }}
        
        Input: "Hello how are you today?"
        Output: {{
            "function_called": "N/A"
        }}
        
        Input: "I want Sportsbook only"
        Output: {{
            "function_called": "N/A"
        }}
        
        Input: "I want change to a little bit, I want to get Product Virtual Sports and product detail Saba Basketball with user level Super Agent"
        Output: {{
            "function_called": "N/A"
        }}
        
        Input: "I want to get the top 20 outstanding"
        Output: {{
            "function_called": "/topoutstanding"
        }}
        
        Input: "The outstanding of Master1"
        Output: {{
            "function_called": "/outstanding"
        }}
        
        Input: "Top 40 Outstanding of Sportsbook"
        Output: {{
            "function_called": "/topoutstanding"
        }}
        
        Input: "My current outstanding"
        Output: {{
            "function_called": "/outstanding"
        }}
        
        Input: "Top 10 Outstanding of Sportsbook"
        Output: {{
            "function_called": "/topoutstanding"
        }}
        
        2. Abbreviation calling
        
        Input: "I want to get wl report for day 10"
        Output: {{
            "function_called": "/winlost_detail"
        }}
        
        Input: "I want to get w/l report for day 10" 
        Output: {{
            "function_called": "/winlost_detail"
        }}
        
        Input: "Show me the WL detail report"
        Output: {{
            "function_called": "/winlost_detail"
        }}
        
        Input: "I want to get TO report"
        Output: {{
            "function_called": "/turnover_detail"
        }}
        
        Input: "TO report please"
        Output: {{
            "function_called": "/turnover_detail"
        }}
        
        Input: "TO report day 15"
        Output: {{
            "function_called": "/turnover_detail"
        }}
        
        Input: "I want to get revenue report"
        Output: {{
            "function_called": "/turnover_detail"
        }}
    """
    system_prompt: str = """
        You are an AI assistant that helps determine which function to call based on user's query.
    """
    user_prompt: str = """
        User request: {message}

        {instruction}
        
        {few_shot}
        
        Based on this request, which function should be called? Return only the JSON response.
    """
    format_schema: Dict[str, Any] = dataclasses.field(default_factory=lambda: {
        "type": "object",
        "properties": {
            "function_called": {
                "type": "string",
                "description": "The name of the function to call",
                "enum": [
                    '/winlost_detail',
                    '/turnover',
                    '/outstanding',
                    '/topoutstanding',
                    'N/A'
                ]
            }
        },
        "required": ["function_called"]
    })
    
    def format_prompt(self, message: str, **kwargs) -> str:
        user_prompt = self.user_prompt.format(
            message=message, 
            instruction=self.instruction.format(
                abbreviation=kwargs['abbreviation'],
                function_description=kwargs['function_description']
            ), 
            few_shot=self.few_shot
        )
        return user_prompt

@dataclasses.dataclass
class ReportCallingAgentConfigV2:
    instruction: str = """
        # General conversation guidelines:
        - Please help me identify which function is being referenced in the user's query based on common abbreviations and variations
        - If the user request contains the word such as "this report", "current report", "last report", "previous report", etc, return "N/A" 
        - Return your answer in JSON format with a single key "function_called"
        - The available abbreviations are:
        {abbreviation}
        - Available functions:
        {function_description}
    """
    
    few_shot: str = f"""
    # ***Example Scenarios:***
    
    - ***User***: "this report is for sportsbook"
    - ***Assistant***: {{ "function_called": "N/A" }}
    
    - ***User***: "the current report is for number game"
    - ***Assistant***: {{ "function_called": "N/A" }}
    
    - ***User***: "I want to get wl report for day 10"
    - ***Assistant***: {{"function_called": "/winlost_detail"}}
    
    - ***User***: "I want to get w/l report for day 10" 
    - ***Assistant***: {{"function_called": "/winlost_detail"}}
    
    - ***User***: "Show me the WL detail report"
    - ***Assistant***: {{"function_called": "/winlost_detail"}}
    
    - ***User***: "I want to get to report"
    - ***Assistant***: {{"function_called": "/turnover_detail"}}
    
    - ***User***: "I want to get revenue report"
    - ***Assistant***: {{"function_called": "/turnover_detail"}}
    """
    
    system_prompt: str = """
    You are a helpful assistant that identifies which function is abbreviated by user's query
    """
    
    user_prompt: str = """
        User request: {message}

        {instruction}
        
        {few_shot}
        
        Based on this request, which function should be called? Return only the JSON response.
    """
    
    format_schema: Dict[str, Any] = dataclasses.field(default_factory=lambda: {
        "type": "object",
        "properties": {
            "function_called": {
                "type": "string",
                "description": "The name of the function to call",
                "enum": [
                    '/winlost_detail',
                    '/turnover',
                    '/outstanding',
                    '/topoutstanding',
                    'N/A'
                ]
            }
        },
        "required": ["function_called"]
    })
    
    def format_prompt(self, message: str, **kwargs) -> str:
        user_prompt = self.user_prompt.format(
            message=message, 
            instruction=self.instruction.format(
                abbreviation=kwargs['abbreviation'],
                function_description=kwargs['function_description']
            ), 
            few_shot=self.few_shot
        )
        return user_prompt

@dataclasses.dataclass
class AbbreviationDateRangeExclusionAgentConfig:
    instructions: str= """
    # Define your task:
    - Extract the most relevant keywords from the following sentence: '{query}'. 
    - You must detect all the keywords based on the abbreviation below:
        {abbreviated_parameters}
    - Return the following format output:
        {{
            "product": "<product_name>",
            "product_detail": "<product_detail_name>",
            "level": "<level_name>"
        }}     
    - If the product is not specified, please return 'All' for product.
    - If the product_detail is not specified, please return 'All' for product_detail.
    - If the level is not specified, please return 'All' for level.
    """
    
    few_shot: str = f"""
    # ***Example Scenarios:***
    
    - ***User***: "SBB please"
    - ***Assistant***: {{"product": "All", "product_detail": "SABA Basketball", "level": "All"}}
    
    - ***User***: "I want to get wl report for SBEPG and SB"
    - ***Assistant***: {{"product": "Sportsbook", "product_detail": "SABA E-Sports PinGoal", "level": "All"}}
    
    - ***User***: "SB please for wl report"
    - ***Assistant***: {{"product": "Sportsbook", "product_detail": "Sportsbook", "level": "All"}} 
    
    - ***User***: "Give me wl report for Num GAME" 
    - ***Assistant***: {{"product": "Number Game", "product_detail": "All", "level": "All"}}
    
    - ***User***: "Show me the WL detail report for sag"
    - ***Assistant***: {{"product": "SA Gaming", "product_detail": "All", "level": "All"}}
    
     - ***User***: "I want to know wl report for sb basket pin and funky games please"
    - ***Assistant***: {{"product": "Funky Games", "product_detail": "SABA Basketball PinGoal", "level": "All"}}
    """
    
    system_prompt: str = """
        You are an AI assistant majoring for Named Entity Recognition trained to extract entity and categorize queries for Winlost Report Detail
    """
    
    user_prompt: str = """
    User's message: {query}
    
    {instructions}
    
    {few_shot}
    """
    
    format_schema: Dict[str, Any] = dataclasses.field(default_factory=lambda: {
        "type": "object",
        "properties": {
            "product": {
                "type": "string"
            },
            "product_detail": {
                "type": "string"
            },
            "level": {
                "type": "string"
            }
        },
        "required": ["product", "product_detail", "level"]
    })
    
    def format_prompt(self, query: str, abbreviated_parameters: List[str]) -> str:
        return self.user_prompt.format(
            query=query,
            instructions=self.instructions.format(
                query=query,
                abbreviated_parameters=abbreviated_parameters
            ),
            few_shot=self.few_shot
        )
    
@dataclasses.dataclass
class DateRangeNERConfig:
    instruction: str = """
        # Define your task:
        - Extract the most relevant keywords from the following query: '{query}'. 
        - Focus on important nouns that convey the core meaning. 
        - Detect any words related to dates such as tomorrow, today, last week, next year, so on, following the example below.
        - Help me convert the date range to the format of YYYY-MM-DD to YYYY-MM-DD.
        - You must strictly follow the examples below.
        
        # For date range, please help me convert it to from_date and to_date in DD/MM/YYYY format following these cases:

        1. If a single date is mentioned (e.g. "day 10"):
           - Use current month and year {current_year} and {current_month}
           - Set both from_date and to_date to that date
           Example: "day 10" -> from_date: 10/{current_month}/{current_year}, to_date: 10/{current_month}/{current_year}

        2. If a date range is specified (e.g. "01/02/2024 to 15/02/2024"):
            - Note that in this case, the date range derived from user's query must be DD/MM/YYYY format
            - Keep the dates as specified in DD/MM/YYYY format
           Example: "01/02/2024 to 15/02/2024" -> from_date: 01/02/2024, to_date: 15/02/2024

        3. If relative dates are mentioned:
           - "today" -> Use {current_date} for both
           - "yesterday" -> Use yesterday's date for both from current date {current_date}
           - "last week" -> From {last_monday} to {last_sunday}
           - "last month" -> from_date is 1st of previous month, to_date is last day of previous month from current date {current_date}
           - "last year" -> from_date is Jan 1st of previous year, to_date is Dec 31st of previous year from current date {current_date}
           - "this week" -> from_date is Monday of current week, to_date is today from current date {current_date}
           - "this month" -> from_date is 1st of current month, to_date is today from current date {current_date}
           - "this year" -> from_date is Jan 1st of current year, to_date is today from current date {current_date}
           
        4. If a month range is specified (e.g. "1/1 to 31/1"):
           - Use current year {current_year}
           - Set from_date to first day of specified month 
           - Set to_date to last day of specified month
           Example: "1/1 to 31/1" in {current_year} -> from_date: 01/01/{current_year}, to_date: 31/01/{current_year}
           
        5. If no date is specified:
           - Set date_range as "N/A"
           - Set both from_date and to_date as "N/A"

        6. If the user is not specified, please return 'N/A' for user. 
    """
    few_shot: str = """
        
        # Example 1:
        ## query: Win/Loss details for Product Virtual Sports for user jackie123
        ## Output:
        {{
            "date_range": "N/A",
            "from_date": "N/A",
            "to_date": "N/A",
            "user": "jackie123"
        }}
        Example 2:
        ## query: Get me a Win Loss Detail Report for Direct Member who played Product Detail Sportsbook in Sportsbook Product from 01/02/2024 to 15/02/2024
        ## Output:
        {{
            "date_range": "01/02/2024 to 15/02/2024",
            "from_date": "01/02/2024",
            "to_date": "15/02/2024",
            "user" : "N\A"
        }}
        
        Example 3:
        ## query: Get me a Win Loss Detail Report for Super Agent who played Product Detail SABA Basketball in SABA Basketball Product from 01/02/2024 to 15/02/2024
        ## Output:
        {{
            "date_range": "01/02/2024 to 15/02/2024",
            "from_date": "01/02/2024",
            "to_date": "15/02/2024",
            "user" : "N\A"
        }}
        
        Example 4:
        ## query: Win/Loss details for Product Sportsbook for user123
        ## Output:
        {{
            "date_range": "N/A",
            "from_date": "N/A",
            "to_date": "N/A",
            "user"  : "user123"
        }}
    """
    system_prompt: str = """
    You are an AI assistant majoring for Named Entity Recognition trained to extract entity and categorize queries for Winlost Report Detail
    """
    user_prompt: str = """

        User request: {query}
    
        Current date: {current_date}
        Current year: {current_year}
        Current month: {current_month}

        {instruction}

        {few_shot}
    """
    format_schema: Dict[str, Any] = dataclasses.field(default_factory=lambda: {
        "type": "object",
        "properties": {
            "date_range": {"type": "string"},
            "from_date": {"type": "string"},
            "to_date": {"type": "string"},
            "user" : {"type": "string"}
        },
        "required": ["date_range", "from_date", "to_date", "user"]
    })
    
    def format_prompt(self, query: str) -> str:
        
        current_date = get_current_date()
        current_year = get_current_year()   
        current_month = get_current_month()

        last_monday, last_sunday = get_last_week_dates()
        
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
                last_monday=last_monday,
                last_sunday=last_sunday
            ), 
            few_shot=self.few_shot.format(
                current_month=current_month,
                current_year=current_year,
                last_monday=last_monday,
                last_sunday=last_sunday
            )
        )
        return user_prompt

@dataclasses.dataclass
class ProductNERConfig:

    system_prompt: str = """
    You are an AI assistant majoring for Named Entity Recognition trained to extract entity and categorize queries for Winlost Report Detail
    """
    instruction: str = """
        # Define your task:
        - Extract product information from the following sentence: '{query}'.
        - If no product is specified, return 'All'.
        
        - Here is the list of products you must detect (PLEASE ONLY return product name that is in the list):
        ### PRODUCT = {lowercase_products}
        
        - You must detect all the keywords based on the abbreviation below:
        {abbreviated_parameters}
        
    """
    few_shot: str = """

        - ***User***: Get me a Win Loss Detail Report for Sportsbook
        - ***Assistant***:
        {{
            "product": "Sportsbook"
        }}
        
        - ***User***: i want wl report for product Bitcoin and product detail SABA other sports
        - ***Assistant***:
        {{
            "product": "Bitcoin"
        }}
        
        - ***User***: Win/Loss details for RNG Keno
        - ***Assistant***:
        {{
            "product": "RNG Keno"
        }}
        
        - ***User***: Show me the report
        - ***Assistant***:
        {{
            "product": "All"
        }}
    
        - ***User***: turnover report for btc and sb soccer day 25
        - ***Assistant***: 
        {{
            "product": "Bitcoin"
        }}
        
        - ***User***: give me top 24 for NSP
        - ***Assistant***: 
        {{
            "product": "Nextspin"
        }}
        
        - ***User***: "I want to get wl report for SBEPG and SB"
        - ***Assistant***: 
        {{
            "product": "Sportsbook"
        }}
        
        - ***User***: "SB please for wl report"
        - ***Assistant***: 
        {{
            "product": "Sportsbook"
        }} 
        
        - ***User***: "Give me wl report for Num GAME" 
        - ***Assistant***: 
        {{
            "product": "Number Game"
        }}
        
        - ***User***: "Show me the WL detail report for sag"
        - ***Assistant***: 
        {{
            "product": "SA Gaming"
        }}
        
        - ***User***: "I want to know wl report for sb basket pin and funky games please"
        - ***Assistant***: 
        {{
            "product": "Funky Games"
        }}
    """
    user_prompt: str = """
        User request: {query}
        
        {instruction}
        
        {few_shot}
    """
    format_schema: Dict[str, Any] = dataclasses.field(default_factory=lambda: {
        "type": "object",
        "properties": {
            "product": {"type": "string"}
        },
        "required": ["product"]
    })
    
    def format_prompt(self, query: str, product_enums: List[str], abbreviated_parameters: List[str]) -> str:

        instruction_with_products = self.instruction.format(
            query=query, 
            lowercase_products=product_enums,
            abbreviated_parameters=abbreviated_parameters
        )
        return self.user_prompt.format(
            query=query,
            instruction=instruction_with_products,
            few_shot=self.few_shot
        )

@dataclasses.dataclass
class ProductDetailNERConfig:
    system_prompt: str = """
    You are an AI assistant majoring for Named Entity Recognition trained to extract entity and categorize queries for Winlost Report Detail
    """

    instruction: str = """
        # Define your task:
        - Extract product detail information from the following sentence: '{query}'.
        - If no product detail is specified, return 'All'.
        
        - Here is the list of product details you should detect (PLEASE ONLY return product detail name that is in the list):
        ### PRODUCT_DETAIL = {lowercase_product_details}
        
        - You must detect all the keywords based on the abbreviation below:
        {abbreviated_parameters}
    """
    few_shot: str = """
        - ***User***: Get me a Win Loss Detail Report for Product Detail Sportsbook
        - ***Assistant***:
        {{
            "product_detail": "Sportsbook"
        }}
        
        - ***User***: Win/Loss details for Product Detail SABA Basketball
        - ***Assistant***:
        {{
            "product_detail": "SABA Basketball"
        }}
        
        - ***User***: Show me the report
        - ***Assistant***:
        {{
            "product_detail": "All"
        }}
        
        - ***User***: turnover report for btc and sb soccer day 25
        - ***Assistant***:
        {{
            "product_detail": "SABA Soccer"
        }}
        
        - ***User***: "SBB please"
        - ***Assistant***:
        {{
            "product_detail": "SABA Basketball"
        }}
        
        - ***User***: i want wl report for product Bitcoin and product detail SABA other sports
        - ***Assistant***:
        {{
            "product_detail": "SABA Other Sports"
        }}
        
        - ***User***: "I want to get wl report for SBEPG and SB"
        - ***Assistant***:
        {{
            "product_detail": "SABA E-Sports PinGoal"
        }}
        
        - ***User***: "SB please for wl report"
        - ***Assistant***:
        {{
            "product_detail": "Sportsbook"
        }} 
        
        - ***User***: "Give me wl report for Num GAME" 
        - ***Assistant***:
        {{
            "product_detail": "All"
        }}
        
        - ***User***: "Show me the WL detail report for sag"
        - ***Assistant***:
        {{
            "product_detail": "SA Gaming"
        }}
        
        - ***User***: "I want to know wl report for sb basket pin and funky games please"
        - ***Assistant***:
        {{
            "product_detail": "SABA Basketball PinGoal"
        }}
    """
    user_prompt: str = """  
        User request: {query}
        
        {instruction}
        
        {few_shot}
    """
    format_schema: Dict[str, Any] = dataclasses.field(default_factory=lambda: {
        "type": "object",
        "properties": {
            "product_detail": {"type": "string"}
        },
        "required": ["product_detail"]
    })
    
    def format_prompt(self, query: str, product_detail_enums: List[str], abbreviated_parameters: List[str]) -> str:
        instruction_with_product_details = self.instruction.format(
            query=query, 
            lowercase_product_details=product_detail_enums,
            abbreviated_parameters=abbreviated_parameters
        )
        return self.user_prompt.format(
            query=query,
            instruction=instruction_with_product_details,
            few_shot=self.few_shot
        )

@dataclasses.dataclass
class LevelNERConfig:
    system_prompt: str = """
    You are an AI assistant majoring for Named Entity Recognition trained to extract entity and categorize queries for Winlost Report Detail
    """

    instruction: str = """
        # Define your task:
        Extract level information from the following sentence: '{query}'.
        If no level is specified, return 'All'.
        
        Here is the list of levels you should detect:
        ### LEVEL = {lowercase_levels}
        
        - You must detect all the keywords based on the abbreviation below:
        {abbreviated_parameters}
    """
    few_shot: str = """
        - ***User***: Get me a Win Loss Detail Report for Direct Member
        - ***Assistant***:
        {{
            "level": "Direct Member"
        }}

        - ***User***: Win/Loss details for Super Agent
        - ***Assistant***:
        {{
            "level": "Super Agent"
        }}
        

        - ***User***: Show me the report
        - ***Assistant***:
        {{
            "level": "All"
        }}
        
        - ***User***: "SBB please"
        - ***Assistant***:
        {{
            "level": "All"
        }}
        
        - ***User***: "I want to get wl report for user level MA"
        - ***Assistant***:
        {{
            "level": "Master Agent"
        }}
        
        - ***User***: "Give me wl report for sb only last week
"
        - ***Assistant***:
        {{
            "level": "All"
        }}
        
        - ***User***: "SB please for wl report user leve AG"
        - ***Assistant***:
        {{
            "level": "Agent"
        }} 
        
        - ***User***: "Give me wl report for Num GAME user level DM" 
        - ***Assistant***:
        {{
            "level": "Direct Member"
        }}
        
        - ***User***: "Show me the WL detail report for sag user level SA"
        - ***Assistant***:
        {{
            "level": "Super Agent"
        }}
        
        - ***User***: "I want to know wl report for sb basket pin and funky games please user level AG"
        - ***Assistant***:
        {{
            "level": "Agent"
        }}
    """
    user_prompt: str = """
        User request: {query}
        
        {instruction}
        
        {few_shot}
    """
    format_schema: Dict[str, Any] = dataclasses.field(default_factory=lambda: {
        "type": "object",
        "properties": {
            "level": {"type": "string"}
        },
        "required": ["level"]
    })
    
    def format_prompt(self, query: str, level_enums: List[str], abbreviated_parameters: List[str]) -> str:

        instruction_with_levels = self.instruction.format(
            query=query, 
            lowercase_levels=level_enums,
            abbreviated_parameters=abbreviated_parameters
        )
        return self.user_prompt.format(
            query=query,
            instruction=instruction_with_levels,
            few_shot=self.few_shot
        )

@dataclasses.dataclass
class WinlostTurnoverNERAgentConfig:
    date_range_config: DateRangeNERConfig = dataclasses.field(default_factory=lambda: DateRangeNERConfig())
    product_config: ProductNERConfig = dataclasses.field(default_factory=lambda: ProductNERConfig())
    product_detail_config: ProductDetailNERConfig = dataclasses.field(default_factory=lambda: ProductDetailNERConfig())
    level_config: LevelNERConfig = dataclasses.field(default_factory=lambda: LevelNERConfig())

    def format_date_range_prompt(self, query: str, parameter_properties: List[str]) -> str:
        return self.date_range_config.format_prompt(query, parameter_properties)
    
    def format_product_prompt(self, query: str, product_enums: List[str]) -> str:
        return self.product_config.format_prompt(query, product_enums)
    
    def format_product_detail_prompt(self, query: str, product_detail_enums: List[str]) -> str:
        return self.product_detail_config.format_prompt(query, product_detail_enums)
    
    def format_level_prompt(self, query: str, level_enums: List[str]) -> str:
        return self.level_config.format_prompt(query, level_enums)
    
@dataclasses.dataclass
class AbbreviationWinlostTurnoverNERAgentConfig:
    date_range_config: DateRangeNERConfig = dataclasses.field(default_factory=lambda: DateRangeNERConfig())
    product_config: ProductNERConfig = dataclasses.field(default_factory=lambda: ProductNERConfig())
    product_detail_config: ProductDetailNERConfig = dataclasses.field(default_factory=lambda: ProductDetailNERConfig())
    level_config: LevelNERConfig = dataclasses.field(default_factory=lambda: LevelNERConfig())

    def format_date_range_prompt(self, query: str) -> str:
        return self.date_range_config.format_prompt(query)

    def format_product_prompt(self, query: str, product_enum: List[str], abbreviated_parameters: List[str]) -> str:
        return self.product_config.format_prompt(query, product_enum, abbreviated_parameters)
    
    def format_product_detail_prompt(self, query: str, product_detail_enum: List[str], abbreviated_parameters: List[str]) -> str:
        return self.product_detail_config.format_prompt(query, product_detail_enum, abbreviated_parameters)
    
    def format_level_prompt(self, query: str, level_enum: List[str], abbreviated_parameters: List[str]) -> str:
        return self.level_config.format_prompt(query, level_enum, abbreviated_parameters)

@dataclasses.dataclass
class AbbreviationOutstandingNERAgentConfig:
    instruction: str = """
    # Define your task:
    - Extract the most relevant keywords from the following sentence: '{query}'. 
    - You must detect all the keywords based on the abbreviation below:
        {abbreviated_parameters}
    - Here is the list of products you must detect (PLEASE ONLY return product name that is in the list):
        ### PRODUCT = {products}
    - Return the following format output:
        {{
            "product": "<product_name>",
            "user": "<user_name>"
        }}     
    - If the product is not specified, please return 'All' for product.
    - If the user is not specified, please return 'N/A' for user.
    """
    few_shot: str = """

        ## User: I want sprtbook only
        ## Output:
        {{
            "product": "Sportsbook",
            "user": "N/A"
        }}
        
        ## User: The outstanding of Master1 for num game
        ## Output:
        {{
            "product": "Number Game",
            "user": "Master1"
        }}
        
        ## User: Outstanding report for sg
        ## Output:
        {{
            "product": "SG",
            "user": "N/A"
        }}
        
        ## User: Give me the outstanding report for Saba Promotion
        ## Output:
        {{
            "product": "Saba Promotion",
            "user": "N/A"
        }}
        
        ## User: I want to get outstanding report for IBCBet Live Casino
        ## Output:
        {{
            "product": "IBCBet Live Casino",
            "user": "N/A"
        }}
    """
    system_prompt: str = """
    You are an AI assistant majoring for Named Entity Recognition trained to extract entity and categorize queries for Outstanding Report Detail
    """
    user_prompt: str = """

        User request: {query}

        {instruction}

        {few_shot}
    """
    format_schema: Dict[str, Any] = dataclasses.field(default_factory=lambda: {
        "type": "object",
        "properties": {
            "product": {"type": "string"},
            "user": {"type": "string"}
        },
        "required": ["product", "user"]
    })
    
    def format_prompt(self, query: str, **kwargs) -> str:
        
        user_prompt = self.user_prompt.format(
            query=query, 
            instruction=self.instruction.format(
                query=query,
                abbreviated_parameters=kwargs['abbreviated_parameters'],
                products=kwargs['products']
            ), 
            few_shot=self.few_shot
        )
        return user_prompt
 
@dataclasses.dataclass
class AbbreviationTopOutstandingNERAgentConfig:
    instruction: str = """
    # Define your task:
    - Extract the most relevant keywords from the following sentence: '{query}'. 
        {abbreviated_parameters}
    - Here is the list of products you must detect (PLEASE ONLY return product name that is in the list):
        ### PRODUCT = {products}
    - Return the following format output:
        {{
            "product": "<product_name>",
            "top": "<top_number>"
        }}     
    - If the product is not specified, please return 'All' for product.
    - If the top is not specified, please return 10 for top.
    """
    few_shot: str = """

        ## User: I want to get top outstanding for sb only
        ## Output:
        {{
            "product": "Sportsbook",
            "top": 10
        }}


        ## User: Top 40 Outstanding of Allbet
        ## Output:
        {{
            "product": "Allbet",
            "top": 40
        }}
        
        ## User: give me the first 20 outstanding sorting from highest to lowest for btc
        ## Output:
        {{
            "product": "Bitcoin",
            "top": 20
        }}
        
        ## User: give me the first 70 outstanding decreasing for yb
        ## Output:
        {{
            "product": "YeeBet",
            "top": 70
        }}
        
        ## User: Limit to top 100 FOR l22
        ## Output:
        {{
            "product": "Live22",
            "top": 100
        }}
        
        ## User: Please give me the top 1 outstanding for sbc
        ## Output:
        {{
            "product": "Saba Coins",
            "top": 1
        }}
        
        ## User: top 200 outstanding for fc
        ## Output:
        {{
            "product": "FA CHAI",
            "top": 200
        }}
        
        ## User: give me top 25 for Saba Virtual Sports
        ## Output:
        {{
            "product": "Saba Virtual Sports",
            "top": 25
        }}
        
        ## User: I want to get top 62 for Yolo Play
        ## Output:
        {{
            "product": "Yolo Play",
            "top": 62
        }}
    """
    system_prompt: str = """
    You are an AI assistant majoring for Named Entity Recognition trained to extract entity and categorize queries for Outstanding Report Detail
    """
    user_prompt: str = """

        User request: {query}

        {instruction}

        {few_shot}
    """
    format_schema: Dict[str, Any] = dataclasses.field(default_factory=lambda: {
        "type": "object",
        "properties": {
            "product": {"type": "string"},
            "top": {"type": "integer"}
        },
        "required": ["product", "top"]
    })
    
    def format_prompt(self, query: str, **kwargs) -> str:
        
   
        user_prompt = self.user_prompt.format(
            query=query, 
            instruction=self.instruction.format(
                query=query,
                abbreviated_parameters=kwargs['abbreviated_parameters'],
                products=kwargs['products']
            ), 
            few_shot=self.few_shot
        )
        return user_prompt
    
@dataclasses.dataclass
class OutstandingNERAgentConfig:
    instruction: str = """
        # Define your task:
        Extract the most relevant keywords from the following sentence: '{query}'. 
        Focus on important nouns that convey the core meaning. 
        If no relevant keywords are detected, return 'All'
        If the product is not specified, please return 'All' for product.
        If the user is not specified, please return 'N/A' for username.

        
        Here is the list of product you should detect:
        {parameter_properties}
    """
    few_shot: str = """
        # Example 1:
        ## User: My current outstanding
        ## Output:
        {{
            "product": "All",
            "user": "N/A"
        }}
        
        Example 2:
        ## User: I want Sportsbook only
        ## Output:
        {{
            "product": "Sportsbook",
            "user": "N/A"
        }}
        
        Example 3:
        ## User: The outstanding of Master1
        ## Output:
        {{
            "product": "All",
            "user": "Master1"
        }}
        
        Example 4:
        ## User: Outstanding report for Product Sportsbook
        ## Output:
        {{
            "product": "Sportsbook",
            "user": "N/A"
        }}
    """
    system_prompt: str = """
    You are an AI assistant majoring for Named Entity Recognition trained to extract entity and categorize queries for Outstanding Report Detail
    """
    user_prompt: str = """

        User request: {query}

        {instruction}

        {few_shot}
    """
    format_schema: Dict[str, Any] = dataclasses.field(default_factory=lambda: {
        "type": "object",
        "properties": {
            "product": {"type": "string"},
            "user": {"type": "string"}
        },
        "required": ["product", "user"]
    })
    
    def format_prompt(self, query: str, **kwargs) -> str:
        
        user_prompt = self.user_prompt.format(
            query=query, 
            instruction=self.instruction.format(
                query=query,
                parameter_properties=kwargs['parameter_properties'],
                # abbreviation=kwargs['abbreviation']
            ), 
            few_shot=self.few_shot
        )
        return user_prompt

@dataclasses.dataclass
class TopOutstandingNERAgentConfig:
    instruction: str = """
        # Define your task:
        Extract the most relevant keywords from the following sentence: '{query}'. 
        Focus on important nouns that convey the core meaning. 
        If no relevant keywords are detected, return 'All'
        If the product is not specified, please return 'All' for product.
        If the top is not specified, please return 10 for top.
        You must detect correctly the top number from the query.
        
        Here is the list of product you should detect:
        {parameter_properties}
    """
    few_shot: str = """
        # Example 1:
        ## User: I want to get top outstanding
        ## Output:
        {{
            "product": "All",
            "top": 10
        }}
        
        Example 2:
        ## User: Top 40 Outstanding of Sportsbook
        ## Output:
        {{
            "product": "Sportsbook",
            "top": 40
        }}
        
        Example 3:
        ## User: give me the first 20 outstanding sorting from highest to lowest
        ## Output:
        {{
            "product": "All",
            "top": 20
        }}
        
        Example 4:
        ## User: give me the first 70 outstanding decreasing
        ## Output:
        {{
            "product": "All",
            "top": 70
        }}
        
        Example 5:
        ## User: Limit to top 100
        ## Output:
        {{
            "product": "All",
            "top": 100
        }}
        
        Example 6:
        ## User: Please give me the top 1 outstanding
        ## Output:
        {{
            "product": "All",
            "top": 1
        }}
        
        Example 7:
        ## User: top 200 outstanding for Number Game
        ## Output:
        {{
            "product": "Number Game",
            "top": 200
        }}
    """
    system_prompt: str = """
    You are an AI assistant majoring for Named Entity Recognition trained to extract entity and categorize queries for Outstanding Report Detail
    """
    user_prompt: str = """

        User request: {query}

        {instruction}

        {few_shot}
    """
    format_schema: Dict[str, Any] = dataclasses.field(default_factory=lambda: {
        "type": "object",
        "properties": {
            "product": {"type": "string"},
            "top": {"type": "integer"}
        },
        "required": ["product", "top"]
    })
    
    def format_prompt(self, query: str, **kwargs) -> str:
        
   
        user_prompt = self.user_prompt.format(
            query=query, 
            instruction=self.instruction.format(
                query=query,
                parameter_properties=kwargs['parameter_properties'],
                # abbreviation=kwargs['abbreviation']
            ), 
            few_shot=self.few_shot
        )
        return user_prompt

@dataclasses.dataclass
class NerAgentConfig:
    winlost_turnover_ner_agent_config: WinlostTurnoverNERAgentConfig = WinlostTurnoverNERAgentConfig
    outstanding_ner_agent_config: OutstandingNERAgentConfig = OutstandingNERAgentConfig
    top_outstanding_ner_agent_config: TopOutstandingNERAgentConfig = TopOutstandingNERAgentConfig
    
    
    def get_agent(self, function_called: str) -> Any:
    
        agents = {
            "/winlost_detail": self.winlost_turnover_ner_agent_config,
            "/turnover": self.winlost_turnover_ner_agent_config,
            "/outstanding": self.outstanding_ner_agent_config,
            "/topoutstanding": self.top_outstanding_ner_agent_config
        }
        
        return agents[function_called]()
    
@dataclasses.dataclass
class AbbreviationNERAgentConfig:
    winlost_turnover_ner_agent_config: AbbreviationWinlostTurnoverNERAgentConfig = AbbreviationWinlostTurnoverNERAgentConfig
    outstanding_ner_agent_config: AbbreviationOutstandingNERAgentConfig = AbbreviationOutstandingNERAgentConfig
    top_outstanding_ner_agent_config: AbbreviationTopOutstandingNERAgentConfig = AbbreviationTopOutstandingNERAgentConfig
    
    
    def get_agent(self, function_called: str) -> Any:
    
        agents = {
            "/winlost_detail": self.winlost_turnover_ner_agent_config,
            "/turnover": self.winlost_turnover_ner_agent_config,
            "/outstanding": self.outstanding_ner_agent_config,
            "/topoutstanding": self.top_outstanding_ner_agent_config
        }
        
        return agents[function_called]()
