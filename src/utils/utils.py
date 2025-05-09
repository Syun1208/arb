import yaml
import json
import time
import numpy as np
import pickle
import re
import faiss

from colorama import Fore
from colorama import Style
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Dict, Any, Optional, List


def load_bin(path: str) -> faiss.IndexFlatIP:
    cpu_index = faiss.read_index(path)
    return cpu_index

def load_pickle(path: str) -> List[str]:
    with open(path, 'rb') as f:
        return pickle.load(f)

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
    Get the dates from last Monday to Sunday in DD/MM/YYYY format.
    
    Returns:
        tuple[str, str]: A tuple containing (last_monday, last_sunday) in DD/MM/YYYY format
    """
    today = datetime.now(ZoneInfo(time_zone))
    
    # Get last Sunday by getting previous day before Monday of current week
    current_monday = today - timedelta(days=today.weekday())
    last_sunday = current_monday - timedelta(days=1)
    
    # Get last Monday (7 days before last Sunday)
    last_monday = last_sunday - timedelta(days=6)
    
    from_date = last_monday.strftime("%d/%m/%Y")
    to_date = last_sunday.strftime("%d/%m/%Y")
    
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
    
    
def format_date(date: str) -> str:
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


def flatten_list_2d(list_2d: List[List[Any]]) -> List[Any]:
    """
    Flatten a 2D list into a 1D list.
    
    Args:
        list_2d (List[List[Any]]): The 2D list to flatten
        
    Returns:
        List[Any]: The flattened 1D list
    """
    return [item for sublist in list_2d for item in sublist]


def filter_words(query: str, words: List[str]) -> str:
    """
    Filter words from a query that match items in a given list, case insensitive.
    
    Args:
        query (str): The input query string to search
        words (List[str]): List of words to match against
        
    Returns:
        str: The first matching word found, or empty string if no match
    """
    # Convert query to lowercase for case-insensitive matching
    query = query.lower()
    
    # Create pattern matching any word in the list
    pattern = '|'.join(map(re.escape, [w.lower() for w in words]))
    
    # Find all matches
    matches = re.findall(pattern, query)
    
    # Return original casing of first match if found
    if matches:
        match_lower = matches[0]
        # Find original word with matching lowercase
        for word in words:
            if word.lower() == match_lower:
                return word
                
    return ""


def parse_2d_to_2key_2value(input_dict: Dict[str, List[str]]) -> Dict[str, str]:
    """
    Parse a dictionary with list values into a flattened dictionary with individual key-value pairs.
    
    Args:
        input_dict (Dict[str, List[str]]): Dictionary with list values
        e.g. {"Sportsbook": ["SB", "SprtBooks"], "Number Game": ["NG", "Num Game"]}
        
    Returns:
        Dict[str, str]: Flattened dictionary with individual key-value pairs
        e.g. {"Sportsbook": "SB", "Sportsbook": "SprtBooks", "Number Game": "NG", "Number Game": "Num Game"}
    """
    output_dict = {}
    for key, value_list in input_dict.items():
        for value in value_list:
            output_dict[key] = value
    return output_dict


def switch_key_value(input_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Switch the positions of keys and values in a dictionary.
    
    Args:
        input_dict (Dict[str, Any]): Input dictionary to switch
        
    Returns:
        Dict[str, Any]: Dictionary with switched key-value pairs
    """
    return {value: key for key, value in input_dict.items()}


def extract_number(text: str) -> int:
    """
    Extract the first number found in a text string using regular expressions.
    
    Args:
        text (str): The input text to search for numbers
        
    Returns:
        int: The first number found in the text, or None if no number is found
    """
    
    # Find all numbers in the text
    numbers = re.findall(r'\d+', text)
    
    # Return first number found or None if no numbers
    if numbers:
        return int(numbers[0])
    return None

def get_most_common(items: List[str]) -> str:
    """
    Get the most common item in a list.
    
    Args:
        items (List[str]): The list of items to check
        
    Returns:
        str: The most common item in the list
    """
    if not items:
        return None
    
    counts = {}
    max_count = 0
    most_common = None
    
    for item in items:
        if item in counts:
            counts[item] += 1
        else:
            counts[item] = 1
            
        if counts[item] > max_count:
            max_count = counts[item]
            most_common = item
            
    return most_common


def get_item_statistics(items: List[List[str]], weights: List[float]) -> str:
    if len(items) != len(weights):
        raise ValueError("Length of items and weights must match")
    
    def compute_prob(item, weight):
        prob = {}
        for i in item:
            if i not in prob:
                prob[i] = 0
            prob[i] += 1 / len(item) * weight
        return prob
    
    prob_items = []
    for i, item in enumerate(items):
        prob_item = compute_prob(item, weights[i])
        prob_items.append(prob_item)
        
    return prob_items

def get_highest_confidence(items: List[List[str]], weights: List[float]) -> str:
    prob_items = get_item_statistics(items, weights)

    probs = []
    items = []
    for i in prob_items:
        probs.extend(list(i.values()))
        items.extend(list(i.keys()))
        
    sorted_prob = np.array(probs).argsort()[::-1]
    sorted_items = np.array(items)[sorted_prob].tolist()

    return sorted_items

def weighted_voting(items: List[List[str]], weights: List[float]) -> str:
    
    prob_items = get_item_statistics(items, weights)
    
    # Calculate average probability for each unique item
    final_probs = {}
    for prob_dict in prob_items:
        for item, prob in prob_dict.items():
            if item not in final_probs:
                final_probs[item] = []
            final_probs[item].append(prob)
    
    # Average the probabilities
    avg_probs = {}
    for item, probs in final_probs.items():
        avg_probs[item] = sum(probs) / len(probs)
    
    # Find item with highest probability
    predicted_item = max(avg_probs.keys(), key=lambda x: avg_probs[x])
    
    return predicted_item
