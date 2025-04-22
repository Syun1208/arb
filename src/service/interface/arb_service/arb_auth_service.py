from abc import ABC, abstractmethod
from typing import Dict

class ARBAuthService(ABC):
    """Abstract base class for authentication service"""
    
    @abstractmethod
    def generate_api_key(self, department: str) -> str:
        """Generate API key for a department
        
        Args:
            department (str): Department name requesting the API key
            
        Returns:
            Dict[str, str]: Dictionary containing the generated API key
        """
        pass
    
    @abstractmethod 
    def verify_api_key(self, api_key: str) -> bool:
        """Verify if an API key is valid
        
        Args:
            api_key (str): API key to verify
            
        Returns:
            bool: True if key is valid, False otherwise
        """
        pass
    
    @abstractmethod
    def delete_api_key(self, department: str) -> bool:
        """Delete API key for a department
        """
        pass

    @abstractmethod
    def get_api_key(self, department: str) -> str:
        """Get API key for a department
        """
        pass
    
    @abstractmethod
    def update_api_key(self, department: str, api_key: str) -> bool:
        """Update API key for a department
        """
        pass
