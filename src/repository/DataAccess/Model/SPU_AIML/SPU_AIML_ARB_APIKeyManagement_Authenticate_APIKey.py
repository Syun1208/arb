from typing import List, Any


class SPU_AIML_ARB_APIKeyManagement_Authenticate_APIKey(object):    
    
    def __init__(self, *args: Any) -> None:
        
        self.ip_APIKey = args[0]
        self.op_ErrorMessage = None

    def __call__(self) -> List[Any]:
        return [
            self.ip_APIKey,
            self.op_ErrorMessage
        ]
