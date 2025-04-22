from abc import ABC, abstractmethod
from typing import Tuple

from src.model.alpha_metadata import AlphaMetadata
from src.model.alpha_status_code import AlphaStatusCode

class AgentComposer(ABC):
    """
    Abstract base class for composing agents.
    """

    @abstractmethod
    async def compose(self, user_id: str, message: str) -> Tuple[AlphaMetadata, AlphaStatusCode]:
        """
        Compose a dictionary of agents.
        """
        pass
