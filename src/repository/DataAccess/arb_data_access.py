from typing import Tuple, Any, Dict

from src.utils.constants import DEPARTMENT_MAPPING_NAME
from src.repository.DataAccess.base_exec_sp import SPExecutor
from src.repository.DataAccess.Model.SPU_AIML.SPU_AIML_ARB_APIKeyManagement_Authenticate_APIKey import SPU_AIML_ARB_APIKeyManagement_Authenticate_APIKey
from src.repository.DataAccess.Model.SPU_AIML.SPU_AIML_ARB_APIKeyManagement_Insert_APIKey import SPU_AIML_ARB_APIKeyManagement_Insert_APIKey
from src.repository.DataAccess.Model.SPU_AIML.SPU_AIML_ARB_APIKeyManagement_Update_APIKey import SPU_AIML_ARB_APIKeyManagement_Update_APIKey
from src.repository.DataAccess.Model.SPU_AIML.SPU_AIML_ARB_APIKeyManagement_Delete_APIKey import SPU_AIML_ARB_APIKeyManagement_Delete_APIKey
from src.repository.DataAccess.Model.SPU_AIML.SPU_AIML_ARB_APIKeyManagement_Get_APIKey import SPU_AIML_ARB_APIKeyManagement_Get_APIKey
from src.repository.DataAccess.Model.SPU_AIML.SPU_AIML_ARB_Insert_EntityExtraction import SPU_AIML_ARB_Insert_EntityExtraction
from src.repository.DataAccess.data_access_connection import BaseRepository



class WasaAimlARBSPExecutor(SPExecutor):
    
    def __init__(
        self, 
        service_id: int,
        wasa_aiml_connector: BaseRepository
    ) -> None:
        super(WasaAimlARBSPExecutor, self).__init__(wasa_aiml_connector)
        self.service_id = service_id
        
    def get_api_key(self, department: str) -> Tuple[Any]:
        department_id = DEPARTMENT_MAPPING_NAME.index(department)
        sp_result = self.manage_sp_operation(
            "SPU_AIML_ARB_APIKeyManagement_Get_APIKey", 
            lambda: SPU_AIML_ARB_APIKeyManagement_Get_APIKey(
                department_id
            )
        )
        
        return sp_result
    
    def verify_api_key(self, api_key: str) -> Tuple[Any]:
        sp_result = self.manage_sp_operation(
            "SPU_AIML_ARB_APIKeyManagement_Authenticate_APIKey", 
            lambda: SPU_AIML_ARB_APIKeyManagement_Authenticate_APIKey(
                api_key
            )
        )
        
        return sp_result

    def delete_api_key(self, department_id: int) -> Tuple[Any]:
        sp_result = self.manage_sp_operation(
            "SPU_AIML_ARB_APIKeyManagement_Delete_APIKey", 
            lambda: SPU_AIML_ARB_APIKeyManagement_Delete_APIKey(
                department_id
            )
        )
        
        return sp_result
    
    def get_api_key(self, department_id: int) -> Tuple[Any]:
        sp_result = self.manage_sp_operation(
            "SPU_AIML_ARB_APIKeyManagement_Get_APIKey", 
            lambda: SPU_AIML_ARB_APIKeyManagement_Get_APIKey(
                department_id
            )
        )
        
        return sp_result
    
    def update_api_key(self, department_id: int, api_key: str) -> Tuple[Any]:
        sp_result = self.manage_sp_operation(
            "SPU_AIML_ARB_APIKeyManagement_Update_APIKey", 
            lambda: SPU_AIML_ARB_APIKeyManagement_Update_APIKey(
                department_id,
                api_key
            )
        )
        
        return sp_result
    
    def insert_api_key(self, department_id: int, api_key: str) -> Tuple[Any]:
        sp_result = self.manage_sp_operation(
            "SPU_AIML_ARB_APIKeyManagement_Insert_APIKey", 
            lambda: SPU_AIML_ARB_APIKeyManagement_Insert_APIKey(
                department_id,
                api_key
            )
        )
        
        return sp_result
    
    def insert_entity_extraction(self, entity_info: Dict[str, Any], running_time: float) -> Tuple[Any]:
        sp_result = self.manage_sp_operation(
            "SPU_AIML_ARB_Insert_EntityExtraction", 
            lambda: SPU_AIML_ARB_Insert_EntityExtraction(
                self.service_id,
                entity_info,
                running_time
            )
        )
        
        return sp_result
        
    
   
