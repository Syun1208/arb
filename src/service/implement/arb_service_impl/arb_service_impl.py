from typing import Tuple

from src.service.interface.arb_service.arb_service import ARBService
from src.service.interface.arb_master_agent.agent_composer import AgentComposer
from src.model.alpha_metadata import AlphaMetadata
from src.model.alpha_status_code import AlphaStatusCode



class ARBServiceImpl(ARBService):
    """
    Implementation of ARBService for the Predator chatbot system.
    This class manages multiple AI agents and their interactions for the Predator chatbot.
    """

    def __init__(
        self,
        agent_composer: AgentComposer
    ) -> None:
        """
        Initialize the ARBServiceImpl with the given agent composer.
        
        Args:
            agent_composer: The agent composer to use for the Predator chatbot.
        """
        super(ARBServiceImpl, self).__init__()
        self.agent_composer = agent_composer

    async def chat(self, user_id: str, message: str) -> Tuple[AlphaMetadata, AlphaStatusCode]:
        return await self.agent_composer.compose(user_id, message)