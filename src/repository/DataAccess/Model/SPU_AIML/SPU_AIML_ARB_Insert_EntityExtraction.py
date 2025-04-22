from typing import List, Any


class SPU_AIML_ARB_Insert_EntityExtraction(object):
    
    def __init__(self, *args: Any) -> None:
        
        self.ip_ServiceID = args[0]
        self.ip_EntityInfo = args[1]
        self.ip_RunningTime = args[2]
        self.op_ErrorMessage = None

    def __call__(self) -> List[Any]:

        return [
            self.ip_ServiceID,
            self.ip_EntityInfo,
            self.ip_RunningTime,
            self.op_ErrorMessage
        ]
