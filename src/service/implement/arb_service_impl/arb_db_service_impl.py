import json
import os
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

from src.service.interface.arb_service.arb_db_service import ARBDBService
from src.utils.utils import load_json, to_json
from src.repository.DataAccess.data_access_connection import BaseRepository
from src.repository.DataAccess.arb_data_access import WasaAimlARBSPExecutor
from src.model.db_model import DBModel as db
class ARBDBServiceImpl(ARBDBService):
    """
    Implementation of NoSQLDatabase interface using JSON file storage.
    """

    def __init__(
        self, 
        service_id: int,
        nosql_connector: str,
        sql_connector: BaseRepository,
        expired_time: int
    ) -> None:
        """
        Initialize JsonDatabase with path to JSON file.

        Args:
            json_file_path (str): Path to the JSON file to use as storage
        """
        self.expired_time = expired_time
        self.nosql_path = nosql_connector
        self.wasa_aiml_connector = WasaAimlARBSPExecutor(service_id, sql_connector)
        self.__ensure_folder_exists()
        self.__init_database()

    def __init_database(self) -> None:
        to_json(data={}, path=self.nosql_path)

    def __ensure_folder_exists(self) -> None:
        if not os.path.exists(os.path.dirname(self.nosql_path)):
            os.makedirs(os.path.dirname(self.nosql_path))
    
    def load(self) -> Dict[str, Any]:
        return load_json(path=self.nosql_path)
    
    def get(self, user_id: str) -> Dict[str, List[str]]:
        """
        Retrieve user data from JSON file.

        Args:
            user_id: User ID to query

        Returns:
            Dict[str, List[str]]: User data if found, None otherwise
        """
        
        data = load_json(path=self.nosql_path)
        if not data:
            return data
        return data.get(user_id)

    def insert(self, user_id: str, metadata: List[Dict[str, Any]]) -> bool:
        """
        Insert new user data into JSON file.

        Args:
            user_id: User ID to insert
            metadata: Metadata to insert

        Returns:
            bool: True if insert successful, False otherwise
        """
        try:
            data = load_json(self.nosql_path)
            data[user_id] = metadata

            to_json(data=data, path=self.nosql_path)   
            
            return True
       
        except Exception as e:
            print('🤖 insert error: ', e)
            return False

    def update(self, user_id: str, metadata: Dict[str, Any]) -> bool:
        """
        Update existing user data in JSON file.

        Args:
            user_id: User ID to update
            metadata: Updated metadata

        Returns:
            bool: True if update successful, False otherwise
        """
        try:
            data = load_json(path=self.nosql_path)
            
            if user_id in list(data.keys()):
                data[user_id] = metadata
                to_json(data=data, path=self.nosql_path)
                
                return True
            
            return False
        
        except Exception as e:
            print('🤖 update error: ', e)
            return False

    def delete(self, user_id: str) -> bool:
        """
        Delete user data from JSON file.

        Args:
            user_id: User ID to delete

        Returns:
            bool: True if deletion successful, False otherwise
        """
        try:
            data = load_json(path=self.nosql_path)
            
            if user_id in data:
                del data[user_id]
                to_json(data=data, path=self.nosql_path)
                
                return True
            
            return False
        except Exception as e:
            print('🤖 delete error: ', e)
            return False
        
    def insert_entity_extraction(self, question: str, entities: str, function_called: str, running_time: float) -> bool:
        ip_EntityInfo = json.dumps([{
            db.ARB_ENTITY_EXTRACTION[db.QUESTION]: question,
            db.ARB_ENTITY_EXTRACTION[db.ENTITIES]: entities,
            db.ARB_ENTITY_EXTRACTION[db.FUNCTION_CALLED]: function_called
        }])
        running_time = round(running_time, 2)

        try:
            return self.wasa_aiml_connector.insert_entity_extraction(ip_EntityInfo, running_time)
        except Exception as e:
            raise ValueError(e)   
        
    def clean_conversation(self, expired_time: int = None) -> bool:
        if expired_time is not None:
            self.expired_time = expired_time
            
        data = load_json(path=self.nosql_path)
        current_datetime = datetime.now()

        for user_id, conversation in data.items():
            duration = (current_datetime - datetime.strptime(conversation[-1]['current_time'], '%Y-%m-%d %H:%M:%S')).total_seconds() / 3600
            if duration >= self.expired_time:
                data.pop(user_id)
            
        to_json(data=data, path=self.nosql_path)
        return True

