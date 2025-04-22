import dataclasses
from typing import Dict, Any
@dataclasses.dataclass
class AlphaStatusCode:
    status_code: int
    message: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "status_code": self.status_code,
            "message": self.message
        }