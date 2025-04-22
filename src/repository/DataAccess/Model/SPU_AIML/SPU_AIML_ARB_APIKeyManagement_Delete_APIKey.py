from typing import List, Any


class SPU_AIML_ARB_APIKeyManagement_Delete_APIKey(object):
    
    def __init__(self, *args: Any) -> None:
        
        self.ip_DepartmentID = args[0]
        self.op_ErrorMessage = None
        
    def __call__(self) -> List[Any]:
        return [
            self.ip_DepartmentID,
            self.op_ErrorMessage
        ]
