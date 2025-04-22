import secrets
import json
from typing import Dict
from fastapi import HTTPException

from src.utils.constants import DEPARTMENT_MAPPING_NAME
from src.service.interface.arb_service.arb_auth_service import ARBAuthService
from src.repository.DataAccess.data_access_connection import BaseRepository
from src.repository.DataAccess.arb_data_access import WasaAimlARBSPExecutor


class ARBAuthServiceImpl(ARBAuthService):
    """Implementation of authentication service"""
    
    def __init__(
        self, 
        service_id: int,
        wasa_aiml_connector: BaseRepository
    ) -> None:
        """Initialize auth service
        
        Args:
            database (ARBDBService): Database service
            
        Returns:
            None
        """
        self.wasa_aiml_connector = WasaAimlARBSPExecutor(service_id, wasa_aiml_connector)
        self.service_id = service_id
        
    async def generate_api_key(self, department: str) -> str:
        """Generate API key for a department
        
        Args:
            department (str): Department name requesting the API key
            
        Returns:
            str: Generated API key
        """
        
        # Store API key in database
        department_id = DEPARTMENT_MAPPING_NAME.index(department.capitalize())
        if len(self.wasa_aiml_connector.get_api_key(department_id)[0]) > 0:
            return "This department already exists"       

        # Generate random API key
        api_key = secrets.token_urlsafe(32)
        
        # Insert API key into database
        self.wasa_aiml_connector.insert_api_key(department_id, api_key)
        print(f'🔑 API Key Inserted into SPU_AIML.ARB_APIKeyManagement: {api_key}')
        
        return api_key
    
    async def verify_api_key(self, api_key: str) -> bool:
        """Verify if an API key is valid
        
        Args:
            api_key (str): API key to verify
            
        Returns:
            bool: True if key is valid, False otherwise
        """
        is_authenticated = 0
        
        sp_result = self.wasa_aiml_connector.verify_api_key(api_key)
        if len(sp_result) != 0:
            department_id, is_authenticated = sp_result[0][0]
            department = DEPARTMENT_MAPPING_NAME[department_id]
        
        if is_authenticated:
            print(f"🔓 Department {department} Authenticated 🎉🎊")
            return True
  
        print(f"❌ Could not authenticate this API Key: {api_key} 🔒")
        return False
    
    async def delete_api_key(self, department: str) -> bool:
        """
        Delete API key for a department
        
        Args:
            department (str): Department name requesting the API key
            
        Returns:
            bool: True if delete is successful, False otherwise
        """
        department_id = DEPARTMENT_MAPPING_NAME.index(department.capitalize())
        return self.wasa_aiml_connector.delete_api_key(department_id)
    
    async def get_api_key(self, department: str) -> str:
        """
        Get API key for a department
        
        Args:
            department (str): Department name requesting the API key
            
        Returns:
            str: API key
        """
        department_id = DEPARTMENT_MAPPING_NAME.index(department.capitalize())
        api_key = self.wasa_aiml_connector.get_api_key(department_id)[0][0][0]
        
        return api_key
    
    async def update_api_key(self, department: str, api_key: str) -> bool:
        """
        Update API key for a department
        
        Args:
            department (str): Department name requesting the API key
            api_key (str): New API key
            
        Returns:
            bool: True if update is successful, False otherwise
        """
        department_id = DEPARTMENT_MAPPING_NAME.index(department.capitalize())
        return self.wasa_aiml_connector.update_api_key(department_id, api_key)
