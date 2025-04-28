import dataclasses
from typing import Dict, Any, Optional

@dataclasses.dataclass
class WinlostParams:
    from_date: str
    to_date: str
    product: str
    product_detail: str
    level: str
    user: str
    
    def to_dict(self) -> Dict[str, str]:
        return dataclasses.asdict(self)
    
@dataclasses.dataclass
class TurnoverParams:
    from_date: str
    to_date: str
    product: str
    product_detail: str
    level: str
    user: str

    def to_dict(self) -> Dict[str, str]:
        return dataclasses.asdict(self)
    
@dataclasses.dataclass
class OutstandingParams:
    product: str
    user: str
    
    def to_dict(self) -> Dict[str, str]:
        return dataclasses.asdict(self)
    
@dataclasses.dataclass
class TopOutstandingParams:
    product: str
    top: str
    
    def to_dict(self) -> Dict[str, str]:
        return dataclasses.asdict(self)
    
@dataclasses.dataclass
class Params:
    winlost_params: WinlostParams = WinlostParams
    turnover_params: TurnoverParams = TurnoverParams
    outstanding_params: OutstandingParams = OutstandingParams
    top_outstanding_params: TopOutstandingParams = TopOutstandingParams
    
    def set_params(self, function_called: str, entities: Dict[str, str]) -> None:
        if function_called == "/winlost_detail":
            endpoint_params = self.winlost_params(
                from_date=entities['from_date'],
                to_date=entities['to_date'], 
                product=entities['product'],
                product_detail=entities['product_detail'],
                level=entities['level'],
                user=entities['user']
            )
        elif function_called == "/turnover":
            endpoint_params = self.turnover_params(
                from_date=entities['from_date'],
                to_date=entities['to_date'],
                product=entities['product'],
                product_detail=entities['product_detail'], 
                level=entities['level'],
                user=entities['user']
            )
        elif function_called == "/outstanding":
            endpoint_params = self.outstanding_params(
                product=entities['product'],
                user=entities['user']
            )
        elif function_called == "/topoutstanding":
            endpoint_params = self.top_outstanding_params(
                product=entities['product'],
                top=entities['top']
            )
        
        self.params = endpoint_params
        
    def get_params(self) -> Any:
        return self.params
    
    def to_dict(self) -> Dict[str, str]:
        return self.params.to_dict()

@dataclasses.dataclass
class AlphaMetadata:
    user_id: str
    is_new_session: bool
    is_action: bool
    endpoint: str
    params: Optional[Params]
    response: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "is_new_session": self.is_new_session,
            "is_action": self.is_action,
            "endpoint": self.endpoint,
            "params": self.params.to_dict() if self.params is not None else None,
            "response": self.response,
        }