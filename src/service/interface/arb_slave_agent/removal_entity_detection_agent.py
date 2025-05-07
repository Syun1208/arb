from abc import ABC, abstractmethod
from typing import List



class RemovalEntityDetectionAgent(ABC):
    """
    Abstract base class defining interface for removal entity detection agents.
    """

    @abstractmethod
    def detect_removal_entities(self, message: str, function_called: str) -> List[str]:
        """Detect entities in the query.
        
        Args:
            message: Message to be removed
            
        Returns:
            List[str]: List of entities
        """
        pass
