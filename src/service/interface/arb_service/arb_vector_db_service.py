from typing import List
from abc import ABC, abstractmethod

class ARBVectorDBService(ABC):
    
    @abstractmethod
    def semantic_index(self, content: List[str]) -> None:
        pass
    
    @abstractmethod
    def keyword_index(self, content: List[str]) -> None:
        pass
    
    @abstractmethod
    def semantic_search(self, query: str, top_k: int = 10) -> str:
        pass
    
    @abstractmethod
    def keyword_search(self, query: str, top_k: int = 10) -> str:
        pass
    
    @abstractmethod
    def hybrid_search(self, query: str, top_k: int = 10) -> str:
        pass
    
    @abstractmethod
    def reranking(self, query: str, top_k: int = 10) -> str:
        pass
