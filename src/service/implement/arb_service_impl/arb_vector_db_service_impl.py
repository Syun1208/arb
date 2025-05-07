from sentence_transformers import SentenceTransformer
import torch
import torch.nn as nn
import faiss
import tqdm
import os
import numpy as np
from typing import List
import pickle
import concurrent.futures
from rank_bm25 import BM25Okapi
from sentence_transformers import CrossEncoder

from src.utils.utils import load_bin, load_pickle, get_highest_confidence
from src.utils.constants import WEIGHT_VOTING_SEARCH
from src.service.interface.arb_service.arb_vector_db_service import ARBVectorDBService

class ARBVectorDBServiceImpl(ARBVectorDBService):
    
    def __init__(
        self,
        path_save: str,
        num_workers: int
    ) -> None:

        self.path_save = path_save
        self.num_workers = num_workers
        self.model_embedding = SentenceTransformer("hiieu/halong_embedding")
        self.model_reranking = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-12-v2', max_length=512)

        device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.model_embedding = self.model_embedding.to(device)
        self.model_reranking = self.model_reranking.to(device)
        
        self.__create_dir_save()

    def __create_dir_save(self) -> None:
        dir_path = os.path.dirname(self.path_save['semantic'])
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def semantic_index(self, content: List[str], name: str = None) -> None:
        # indexing
        data_embeddings = self.model_embedding.encode(content)
        
        cpu_index = faiss.IndexFlatIP(768)
        for embedding in tqdm.tqdm(data_embeddings, colour='green', desc='Semantic Indexing'):
            embedding = embedding.astype(np.float32).reshape(1, -1)
            cpu_index.add(embedding)

        # Save vector database
        path_save = self.path_save['semantic']
        if name is not None:
            name_file = os.path.basename(self.path_save['semantic'])
            path_save = os.path.join(os.path.dirname(self.path_save['semantic']), f'{name}_{name_file}')
        faiss.write_index(cpu_index, path_save)

        
    def keyword_index(self, content: List[str], name: str = None) -> None:
        tokenized_corpus = []

        for doc in tqdm.tqdm(content, colour='green', desc='Keyword Indexing'):
            tokenized_corpus.append(doc)

        path_save = self.path_save['keyword']
        if name is not None:
            name_file = os.path.basename(self.path_save['keyword'])
            path_save = os.path.join(os.path.dirname(self.path_save['keyword']), f'{name}_{name_file}')
        with open(path_save, 'wb') as f:
            pickle.dump(tokenized_corpus, f)
        
    def semantic_search(self, query: str, top_k: int = 10, name: str = None) -> str:
        path_save = self.path_save['semantic']
        if name is not None:
            name_file = os.path.basename(self.path_save['semantic'])
            path_save = os.path.join(os.path.dirname(self.path_save['semantic']), f'{name}_{name_file}')

        faiss_index = load_bin(path_save)
        query_embedding = self.model_embedding.encode(query)
        query_embedding = query_embedding.astype(np.float32).reshape(1, -1)
        distances, indices = faiss_index.search(query_embedding, top_k)
        return indices.tolist()[0]

    def keyword_search(self, query: str, top_k: int = 10, name: str = None) -> str:
        path_save = self.path_save['keyword']
        if name is not None:
            name_file = os.path.basename(self.path_save['keyword'])
            path_save = os.path.join(os.path.dirname(self.path_save['keyword']), f'{name}_{name_file}').replace("\\", "/")
        
        bm25_index = load_pickle(path_save)
        bm25 = BM25Okapi(bm25_index)
        docs = bm25.get_top_n(query, bm25_index, n=top_k)
        index = np.where(np.isin(bm25_index, docs))[0].tolist()
        return index

    def hybrid_search(self, query: str, top_k: int = 10, name: str = None) -> str:
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            semantic_future = executor.submit(self.semantic_search, query, top_k, name)
            keyword_future = executor.submit(self.keyword_search, query, top_k, name)
            
            semantic_indexes = semantic_future.result()
            keyword_indexes = keyword_future.result()
            
        confidence_indexes = get_highest_confidence(
            [semantic_indexes, keyword_indexes], 
            [WEIGHT_VOTING_SEARCH['semantic_search'], WEIGHT_VOTING_SEARCH['keyword_search']]
        )
        return confidence_indexes[:top_k]

    def reranking(self, contexts: str, top_k: int = 10) -> str:
        sigmoid = nn.Sigmoid()

        scores = self.model_reranking.predict(contexts, activation_fn=sigmoid)
        
        top_k_values = np.sort(scores)[-top_k:][::-1]
        top_k_indices = np.argsort(scores)[-top_k:][::-1]
        
        best_contexts = np.array(contexts)[top_k_indices].tolist()
        best_contexts = [context[1] for context in best_contexts]
        return best_contexts
