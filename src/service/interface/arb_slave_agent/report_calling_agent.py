from abc import ABC, abstractmethod
from typing import Dict, Any

class ReportCallingAgent(ABC):
    """
    Abstract base class for Report Calling operations.
    This class defines the interface for handling report calling in the system.
    """
    
    @abstractmethod
    def call_report(self, message: str) -> Dict[str, Any]:
        """
        Call a registered report with the given message.
        
        Args:
            message (str): The message to pass to the function
            
        Returns:
            Dict[str, Any]: Result of the function execution
        """
        pass
    
