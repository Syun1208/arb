import dataclasses
from typing import Dict, Any

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

@dataclasses.dataclass
class ReportCallingAgentConfig:
    instruction: str = """
        # ⚠️Note that:
            - If the user request is not related to the function, return "N/A"
            - If the user request is not clear, return "N/A"
            - If the user request is not related to the function, return "N/A"
            - Available functions:
                {function_description}
                
            - Function Abbreviations:
                {abbreviation}

            - Determine which function best matches the user's request and return it in JSON format like:
            {{
                "function_called": "/function_name"
            }}
    """
    few_shot: str = """
        #📝Example requests and responses:
        
        Input: "I need to see the win/loss report from last week"
        Output: {{
            "function_called": "/get_winlost_report"
        }}

        Input: "I want to get the turnover report"
        Output: {{
            "function_called": "/get_turnover_report"
        }}

        Input: "I want to take turnover report for user 123"
        Output: {{
            "function_called": "/get_turnover_report"
        }}

        Input: "Get me the get winlost report for March transactions"
        Output: {{
            "function_called": "/get_winlost_report"
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
    """
    system_prompt: str = """
        You are an AI assistant that helps determine which function to call based on user's query.
    """
    user_prompt: str = """
        User request: {query}

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
                    '/get_winlost_report',
                    # '/get_betcount_report',
                    '/get_turnover_report',
                    # '/get_net_turnover_report',
                    # '/get_gross_comm_report',
                    # '/get_member_report',
                    # '/get_agent_report',
                    # '/get_master_report',
                    # '/get_super_report',
                    # '/get_company_report',
                    # '/get_reward_report',
                    'N/A'
                ]
            }
        },
        "required": ["function_called"]
    })

@dataclasses.dataclass
class NERAgentConfig:
    instruction: str = """
        # Define your task:
        Extract the most relevant keywords from the following sentence: '{query}'. 
        Focus on important nouns that convey the core meaning. 
        Detect any words related to dates such as tomorrow, today, last week, next year, so on, following the example below.
        Help me convert the date range to the format of YYYY-MM-DD to YYYY-MM-DD.
        
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
           - "last week" -> from_date is 7 days ago, to_date is today from current date {current_date}
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
           
        If no relevant keywords are detected, return 'All' (except for dates, you must fill 'N/A').
        If the date range is not specified, please return 'N/A' for date_range.
        If the product is not specified, please return 'All' for product.
        If the product detail is not specified, please return 'All' for product_detail.
        If the level is not specified, please return 'All' for level.
        If the user is not specified, please return 'N/A' for user.
        
        Here is the list of product and product detail you should detect:
        {parameter_properties}
    """
    few_shot: str = """
        # Example 1:
        ## User: Get me a Win Loss Detail Report on day 10
        ## Output:
        {{
            "date_range": "day 10",
            "from_date": "10/{current_month}/{current_year}",
            "to_date": "10/{current_month}/{current_year}",
            "product": "All",
            "product_detail": "All",
            "level": "All",
            "user": "N/A"
        }}
        
        Example 2:
        ## User: Get me a Win Loss Detail Report for Direct Member who played Product Detail Sportsbook in Sportsbook Product from 01/02/2024 to 15/02/2024
        ## Output:
        {{
            "date_range": "01/02/2024 to 15/02/2024",
            "from_date": "01/02/2024",
            "to_date": "15/02/2024",
            "product": "Sportsbook",
            "product_detail": "Sportsbook",
            "level": "Direct Member",
            "user": "N/A"
        }}
        
        Example 3:
        ## User: Get me a Win Loss Detail Report for Super Agent who played Product Detail SABA Basketball in SABA Basketball Product from 01/02/2024 to 15/02/2024
        ## Output:
        {{
            "date_range": "01/02/2024 to 15/02/2024",
            "from_date": "01/02/2024",
            "to_date": "15/02/2024",
            "product": "SABA Basketball",
            "product_detail": "SABA Basketball",
            "level": "Super Agent",
            "user": "N/A"
        }}
        
        Example 4:
        ## User: Win/Loss details for Product Sportsbook
        ## Output:
        {{
            "date_range": "N/A",
            "from_date": "N/A",
            "to_date": "N/A",
            "product": "Sportsbook",
            "product_detail": "All",
            "level": "All",
            "user": "N/A"
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
            "product": {"type": "string"},
            "product_detail": {"type": "string"},
            "level": {"type": "string"},
            "user": {"type": "string"}
        },
        "required": ["date_range", "from_date", "to_date", "product", "product_detail", "level", "user"]
    })


AGREE_PHRASES = [
    "accept",
    "consent",
    "approve",
    "affirm",
    "acknowledge",
    "concur",
    "settle",
    "come to terms",
    "reach an understanding",
    "see eye to eye",
    "be on the same page",
    "align",
    "share the same view",
    "be of the same mind",
    "hold the same opinion",
    "support",
    "sanction",
    "ratify",
    "endorse",
    "authorize",
    "I totally agree",
    "I completely agree",
    "I couldn't agree more",
    "Absolutely!",
    "Exactly!",
    "That's so true",
    "You're absolutely right",
    "I'm with you on that",
    "No doubt about it",
    "That's exactly how I feel",
    "You nailed it",
    "I feel the same way",
    "That's a good point",
    "We're on the same page",
    "I second that",
    "I’m all for it",
    "Preach!",
    "100% agree",
    "Totally!",
    "Couldn't have said it better myself"
]


FUNCTION_MAPPING_NAME = {
    '/get_winlost_report': 'Win Loss Report',
    '/get_betcount_report': 'Bet Count Report', 
    '/get_turnover_report': 'Turnover Report',
    '/get_net_turnover_report': 'Net Turnover Report',
    '/get_gross_comm_report': 'Gross Commission Report',
    '/get_member_report': 'Member Report',
    '/get_agent_report': 'Agent Report',
    '/get_master_report': 'Master Report',
    '/get_super_report': 'Super Report',
    '/get_company_report': 'Company Report',
    '/get_reward_report': 'Reward Report',
    None: 'Could not find the Function/Report, please give me a valid Function/Report'
}

DEPARTMENT_MAPPING_NAME = [
    'Alpha'
] 
