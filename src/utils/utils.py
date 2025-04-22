import yaml
import json
import time

from colorama import Fore
from colorama import Style
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Dict, Any, Optional


def load_yaml(file_path: str):
    try:
        with open(file_path, "r", encoding='utf-8') as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"Error loading YAML file {file_path}: {e}")
        return None
    


def load_json(path) -> Dict[str, Any]:
    with open(path, 'r', encoding="utf-8") as json_file:
        documents = json.load(json_file)
    return documents



def to_json(data, path):
    try:
        with open(path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving JSON file {path}: {e}")
        
        
def get_current_year(time_zone: str = "Etc/GMT-4") -> str:
    """
    Get the current year in YYYY format.
    
    Returns:
        str: Current year in YYYY format
    """
    return datetime.now(ZoneInfo(time_zone)).strftime("%Y")



def get_current_date(time_zone: str = "Etc/GMT-4") -> str:
    """
    Get the current datetime in YYYY-MM-DD format.
    
    Returns:
        str: Current date in YYYY-MM-DD format
    """
    return datetime.now(ZoneInfo(time_zone)).strftime("%Y-%m-%d")



def get_current_month(time_zone: str = "Etc/GMT-4") -> str:
    """
    Get the current month in MM format.
    
    Returns:
        str: Current month in MM format
    """
    return datetime.now(ZoneInfo(time_zone)).strftime("%m")

def get_current_day(time_zone: str = "Etc/GMT-4") -> str:
    """
    Get the current day in DD format.
    
    Returns:
        str: Current day in DD format
    """
    return datetime.now(ZoneInfo(time_zone)).strftime("%d")


def get_current_previous_date(time_zone: str = "Etc/GMT-4") -> str:
    """
    Get the previous date in DD format.
    
    Returns:
        str: Previous date in DD format
    """
    return (datetime.now(ZoneInfo(time_zone)) - timedelta(days=1)).strftime("%d")

def get_last_week_dates(time_zone: str = "Etc/GMT-4") -> tuple[str, str]:
    """
    Get the dates from 7 days ago to today in DD/MM/YYYY format.
    
    Returns:
        tuple[str, str]: A tuple containing (seven_days_ago, today) in DD/MM/YYYY format
    """
    # Get current date
    current_date = datetime.now(ZoneInfo(time_zone))
    
    # Get date from 7 days ago
    seven_days_ago = current_date - timedelta(days=7)
    
    # Format dates as DD/MM/YYYY
    from_date = seven_days_ago.strftime("%d/%m/%Y")
    to_date = current_date.strftime("%d/%m/%Y")
    
    return from_date, to_date

def format_entities_for_prompt(entities: Dict[str, str]) -> str:
    """
    Converts a dictionary of entities into a formatted string representation.
    
    Args:
        entities: Dictionary containing entity key-value pairs
        
    Returns:
        Formatted string with entities listed in bullet points
    """
    formatted_str = ""
    for key, value in entities.items():
        # Convert snake_case to Title Case
        formatted_key = " ".join(word.capitalize() for word in key.split('_'))
        formatted_str += f"- {formatted_key}: '{value}'\n"
    return formatted_str.rstrip()


def get_key_by_value(dictionary: Dict, value_to_find: Any) -> Optional[Any]:
    """
    Find a key in a dictionary based on its value.
    
    Args:
        dictionary (Dict): The dictionary to search in
        value_to_find (Any): The value to look for
        
    Returns:
        Optional[Any]: The key if found, None otherwise
    """
    for key, value in dictionary.items():
        if value == value_to_find:
            return key
    return None


def get_this_week_dates(time_zone: str = "Etc/GMT-4") -> tuple[str, str]:
    """
    Get the dates from Monday of current week to today in DD/MM/YYYY format.
    
    Returns:
        tuple[str, str]: A tuple containing (monday_of_week, today) in DD/MM/YYYY format
    """
    # Get current date
    current_date = datetime.now(ZoneInfo(time_zone))
    
    # Get Monday of current week (weekday() returns 0 for Monday)
    days_since_monday = current_date.weekday()
    monday = current_date - timedelta(days=days_since_monday)
    
    # Format dates as DD/MM/YYYY
    from_date = monday.strftime("%d/%m/%Y")
    to_date = current_date.strftime("%d/%m/%Y")
    
    return from_date, to_date


def get_yesterday_dates(time_zone: str = "Etc/GMT-4") -> str:
    """
    Get yesterday's date in DD/MM/YYYY format.
    
    Returns:
        tuple[str, str]: A tuple containing (yesterday, yesterday) in DD/MM/YYYY format
    """
    yesterday = datetime.now(ZoneInfo(time_zone)) - timedelta(days=1)
    formatted_date = yesterday.strftime("%d/%m/%Y")
    return formatted_date


def get_last_week_dates(time_zone: str = "Etc/GMT-4") -> tuple[str, str]:
    """
    Get the dates from 7 days ago to today in DD/MM/YYYY format.
    
    Returns:
        tuple[str, str]: A tuple containing (7_days_ago, today) in DD/MM/YYYY format
    """
    today = datetime.now(ZoneInfo(time_zone))
    seven_days_ago = today - timedelta(days=7)
    
    from_date = seven_days_ago.strftime("%d/%m/%Y")
    to_date = today.strftime("%d/%m/%Y")
    
    return from_date, to_date


def get_last_month_dates(time_zone: str = "Etc/GMT-4") -> tuple[str, str]:
    """
    Get the first and last day of previous month in DD/MM/YYYY format.
    
    Returns:
        tuple[str, str]: A tuple containing (first_day, last_day) in DD/MM/YYYY format
    """
    today = datetime.now(ZoneInfo(time_zone))
    first_day = today.replace(day=1) - timedelta(days=1)  # Last day of previous month
    last_day = first_day
    first_day = first_day.replace(day=1)  # First day of previous month
    
    from_date = first_day.strftime("%d/%m/%Y")
    to_date = last_day.strftime("%d/%m/%Y")
    
    return from_date, to_date


def get_last_year_dates(time_zone: str = "Etc/GMT-4") -> tuple[str, str]:
    """
    Get the first and last day of previous year in DD/MM/YYYY format.
    
    Returns:
        tuple[str, str]: A tuple containing (first_day, last_day) in DD/MM/YYYY format
    """
    current_year = datetime.now(ZoneInfo(time_zone)).year
    from_date = f"01/01/{current_year-1}"
    to_date = f"31/12/{current_year-1}"
    
    return from_date, to_date


def get_this_month_dates(time_zone: str = "Etc/GMT-4") -> tuple[str, str]:
    """
    Get the first and last day of current month in DD/MM/YYYY format.
    
    Returns:
        tuple[str, str]: A tuple containing (first_day, last_day) in DD/MM/YYYY format
    """
    today = datetime.now(ZoneInfo(time_zone))
    first_day = today.replace(day=1)
    
    # Get last day by getting first day of next month - 1 day
    if today.month == 12:
        last_day = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
    else:
        last_day = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
    
    from_date = first_day.strftime("%d/%m/%Y")
    to_date = last_day.strftime("%d/%m/%Y")
    
    return from_date, to_date



def get_this_year_dates(time_zone: str = "Etc/GMT-4") -> tuple[str, str]:
    """
    Get the first and last day of current year in DD/MM/YYYY format.
    
    Returns:
        tuple[str, str]: A tuple containing (first_day, last_day) in DD/MM/YYYY format
    """
    current_year = datetime.now(ZoneInfo(time_zone)).year
    from_date = f"01/01/{current_year}"
    to_date = f"31/12/{current_year}"
    
    return from_date, to_date


def fancy_print(message: str) -> None:
    """
    Displays a fancy print message.

    Args:
        message (str): The message to display.
    """
    print(Style.BRIGHT + Fore.CYAN + f"\n{'=' * 50}")
    print(Fore.MAGENTA + f"{message}")
    print(Style.BRIGHT + Fore.CYAN + f"{'=' * 50}\n")
    time.sleep(0.5)


def fancy_step_tracker(step: int, total_steps: int) -> None:
    """
    Displays a fancy step tracker for each iteration of the generation-reflection loop.

    Args:
        step (int): The current step in the loop.
        total_steps (int): The total number of steps in the loop.
    """
    fancy_print(f"STEP {step + 1}/{total_steps}")