from typing import Dict, List, Any


class SPU_AIML_ARB_APIKeyManagement_Get_APIKey(object):
    
    def __init__(self, *args: Any) -> None:

        self.ip_DepartmentID: int = args[0]
        self.op_ErrorMessage = None
        
    def __call__(self) -> List[Any]:
        return [
            self.ip_DepartmentID,
            self.op_ErrorMessage
        ]
