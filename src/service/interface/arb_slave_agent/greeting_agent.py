from abc import ABC, abstractmethod

class GreetingAgent(ABC):

    @abstractmethod
    def chat(self, message: str) -> str:
        pass
    