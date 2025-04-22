from abc import ABC, abstractmethod
from typing import Dict


class RecognizerAgent(ABC):
    

    @abstractmethod
    def get_decision(self, query: str) -> Dict[str, int]:
        """
        Abstract method to process the user's query and return a decision.

        Args:
            query (str): The user's query.

        Returns:
            Dict[str, str]: A dictionary containing the decision or confirmation result.
        """
        pass