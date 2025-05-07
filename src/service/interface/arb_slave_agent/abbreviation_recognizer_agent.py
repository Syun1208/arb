from abc import ABC, abstractmethod
from typing import List

from src.model.abbreviation_info import AbbreviationInfo

class AbbreviationRecognizerAgent(ABC):
    
    @abstractmethod
    def index_report_abbreviation(self) -> None:
        pass
    
    @abstractmethod
    def index_entity_abbreviation(self) -> None:
        pass
    
    @abstractmethod
    def recognize_report(self, query: str) -> List[str]:
        pass
    
    @abstractmethod
    def recognize_entity(self, query: str, function_called: str) -> List[AbbreviationInfo]:
        pass
