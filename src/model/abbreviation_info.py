from dataclasses import dataclass

@dataclass
class AbbreviationInfo:
    function: str
    parameter: str
    origin: str
    abbreviation: str
    
    def to_dict(self) -> dict:
        return {
            "function": self.function,
            "parameter": self.parameter,
            "origin": self.origin,
            "abbreviation": self.abbreviation
        }
