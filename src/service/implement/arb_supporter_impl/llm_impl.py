import requests
from typing import Dict, Any, List
from src.service.interface.arb_supporter.llm import LLM


class LLMImpl(LLM):
    
    def __init__(
        self, 
        api: str,
    ) -> None:
        super(LLMImpl, self).__init__()
        
        self.api = api

    def invoke(
        self,
        model: str,
        messages: List[Dict[str, str]],
        tools: Dict[str, Any] = None,
        format_schema: Dict[str, Any] = None,
        endpoint: str = '/api/chat'
    ) -> Dict[str, str]:
        
        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "model": model,
            "messages": messages,
            "stream": False
        }

        if format_schema is not None:
            data = {
                "model": model,
                "messages": messages,
                "format": format_schema,
                "stream": False
            }

        if tools is not None:   
            data = {
                "model": model,
                "messages": messages,
                "tools": tools,
                "stream": False
            }

        url = f'{self.api}{endpoint}'
        response = requests.post(url, headers=headers, json=data, timeout=600)

        if response.status_code != 200:
            raise Exception(f"Request failed with status {response.status_code}: {response.text}")

        response_data = response.json()
        
        return response_data['message']['content']