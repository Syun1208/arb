from typing import Dict, Any, List
import numpy as np
import concurrent.futures

from src.model.abbreviation_info import AbbreviationInfo
from src.service.interface.arb_slave_agent.abbreviation_recognizer_agent import AbbreviationRecognizerAgent
from src.service.implement.arb_service_impl.arb_vector_db_service_impl import ARBVectorDBServiceImpl

class AbbreviationRecognizerAgentImpl(AbbreviationRecognizerAgent):
    
    def __init__(
        self,
        report_vector_db: ARBVectorDBServiceImpl,
        entity_vector_db: ARBVectorDBServiceImpl,
        top_k: int,
        report_config: Dict[str, Any],
        num_workers: int,
    ) -> None:
        super(AbbreviationRecognizerAgentImpl, self).__init__()
        
        self.top_k = top_k
        self.report_config = report_config
        self.report_vector_db = report_vector_db
        self.entity_vector_db = entity_vector_db
        self.num_workers = num_workers
        

    def __get_report_abbreviation(self) -> str:
        function_list = []
        abbreviation_list = []
        for function_called in self.report_config.keys():
            func_info = self.report_config[function_called]
            function_abbreviation = func_info['function']['abbreviation']
            function_list.extend([function_called] * len(function_abbreviation))
            abbreviation_list.extend(function_abbreviation)
        return function_list, abbreviation_list

    def __get_entity_abbreviation(self, function_called: str) -> str:
        abbreviation_info = []
        properties = self.report_config[function_called]['function']['parameters']['properties']
        for param, value in properties.items():
            if "abbreviation" in value:
                
                for origin, abb in value['abbreviation'].items():
                    abbreviation_info.append(
                        AbbreviationInfo(
                            function=function_called,
                            parameter=param,
                            origin=origin,
                            abbreviation=', '.join(abb)
                        )
                    )
        return abbreviation_info
    
    def __convert_data4reranking(self, query: str, entity_abbreviation: List[Any]) -> List[str]:
        contexts = []
        for info in entity_abbreviation:
            
            if isinstance(info, AbbreviationInfo):
                contexts.append((query, info.abbreviation))
                
            if isinstance(info, str):
                contexts.append((query, info))
        return contexts
    
    def index_report_abbreviation(self) -> None:
        _, function_abbreviation = self.__get_report_abbreviation()
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            semantic_future = executor.submit(self.report_vector_db.semantic_index, function_abbreviation)
            keyword_future = executor.submit(self.report_vector_db.keyword_index, function_abbreviation)
            semantic_future.result()
            keyword_future.result()
    
    def index_entity_abbreviation(self) -> None:
        
        for function_called in self.report_config.keys():
            properties = self.report_config[function_called]['function']['parameters']['properties']
            abbreviation_info = []
            
            for param, value in properties.items():
                if "abbreviation" in value:
                    
                    for origin, abb in value['abbreviation'].items():
                        abbreviation_info.append(
                            AbbreviationInfo(
                                function=function_called,
                                parameter=param,
                                origin=origin,
                                abbreviation=', '.join(abb)
                            ).to_dict()
                        )
            abbreviation_list = [info['abbreviation'] for info in abbreviation_info]
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_workers) as executor:
                semantic_future = executor.submit(self.entity_vector_db.semantic_index, abbreviation_list, name=function_called.strip('/'))
                keyword_future = executor.submit(self.entity_vector_db.keyword_index, abbreviation_list, name=function_called.strip('/'))
                semantic_future.result()
                keyword_future.result()

    def recognize_report(self, query: str) -> List[str]:
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            search_future = executor.submit(self.report_vector_db.hybrid_search, query)
            abbreviation_future = executor.submit(self.__get_report_abbreviation)
            
            confidence_indexes = search_future.result()
            function_list, _ = abbreviation_future.result()

        function_list = np.array(function_list)
        function_list = function_list[confidence_indexes].tolist()

        contexts = self.__convert_data4reranking(query, function_list)

        best_contexts = self.report_vector_db.reranking(contexts, top_k=self.top_k)
        best_contexts = np.array(best_contexts)
        
        return best_contexts
    
    def recognize_entity(self, query: str, function_called: str) -> List[AbbreviationInfo]:
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            search_future = executor.submit(self.entity_vector_db.hybrid_search, query, name=function_called.strip("/"))
            abbreviation_future = executor.submit(self.__get_entity_abbreviation, function_called)
            
            confidence_indexes = search_future.result()
            entity_abbreviation = abbreviation_future.result()
        
        entity_abbreviation = np.array(entity_abbreviation)
        entity_abbreviation = entity_abbreviation[confidence_indexes].tolist()
        
        contexts = self.__convert_data4reranking(query, entity_abbreviation)
        
        best_contexts = self.entity_vector_db.reranking(contexts, top_k=self.top_k)
        best_contexts = np.array(best_contexts)

        return best_contexts