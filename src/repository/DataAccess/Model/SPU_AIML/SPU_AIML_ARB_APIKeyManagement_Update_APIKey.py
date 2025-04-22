from typing import Any, List


class SPU_AIML_ARB_APIKeyManagement_Update_APIKey(object):
    
    def __init__(self, *args: Any) -> None:

        self.ip_DepartmentID = args[0]
        self.ip_APIKey = args[1]
        self.op_ErrorMessage = None
        
    def __call__(self) -> List[Any]:
        return [
            self.ip_DepartmentID,
            self.ip_APIKey, 
            self.op_ErrorMessage
        ]
