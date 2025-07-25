# app/services/rag.py

import os
import faiss

from llama_cpp import Llama
from typing import Optional
from app.core.settings import settings
from app.core.logger import logger
from app.utils.prompt import build_prompt
from app.services.base_llm import BaseLLM
from app.services.llama_llm import LlamaLLM
from app.services.ollama_llm import OllamaLLM
from app.services.openai_llm import OpenAILLM
from sentence_transformers import SentenceTransformer


class RAGService:
    def __init__(self):
        logger.debug('Initializing RAG service...')
        self.docs = self._load_documents(settings.DOCS_PATH)
        self.embedding_model = self._load_embedding_model()
        logger.debug(f'Generating embeddings for {len(self.docs)} documents...')
        self.embeddings = self.embedding_model.encode(
            [f'passage: {doc}' for doc in self.docs],
            normalize_embeddings=True
        )
        logger.debug(
                f'Document embeddings generated: {self.embeddings.shape[0]} '
                f'documents, {self.embeddings.shape[1]} dimensions.'
            )
        self.index = self._build_faiss_index(self.embeddings)
        self.llm = self._load_llm()

    def _load_documents(self, path: str) -> list[str]:
        if not os.path.exists(path):
            raise FileNotFoundError(f'Archivo no encontrado: {path}')
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        docs = [doc.strip() for doc in content.split('\n') if doc.strip()]
        logger.info(f'{len(docs)} documents loaded from {path}')
        return docs

    def _load_embedding_model(self) -> SentenceTransformer:
        if os.path.exists(settings.EMBEDDING_MODEL_PATH):
            logger.debug(
                'Local embedding model used: ' +
                settings.EMBEDDING_MODEL_PATH
            )
            return SentenceTransformer(settings.EMBEDDING_MODEL_PATH, local_files_only=True)
        else:
            logger.debug(f'Downloading model: {settings.EMBEDDING_MODEL_NAME}...')
            model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
            model.save(settings.EMBEDDING_MODEL_PATH)
            return model

    def _build_faiss_index(self, embeddings) -> faiss.IndexFlatIP:
        logger.debug('Building FAISS index for similarity search...')
        index = faiss.IndexFlatIP(embeddings.shape[1])
        index.add(embeddings)
        logger.info('FAISS index built.')
        return index

    def _load_llm(self) -> BaseLLM:
        backend = settings.LLM_BACKEND.lower()
        if backend == 'llama':
            logger.debug('Using llama.cpp backend')
            return LlamaLLM()
        elif backend == 'ollama':
            logger.debug('Using Ollama backend')
            return OllamaLLM()
        elif backend == 'openai':
            logger.debug('Using OpenAI backend')
            return OpenAILLM()
        else:
            raise ValueError(f'LLM_BACKEND desconocido: {backend}')

    def retrieve_context(self, query: str) -> str:
        """
        Devuelve el documento más relevante como contexto, o una cadena vacía
        si no se supera el umbral de similitud.
        """
        query_formatted = f'query: {query}'
        query_embedding = self.embedding_model.encode([query_formatted], normalize_embeddings=True)
        logger.debug('Searching for the question embedding in the FAISS index...')
        scores, indices = self.index.search(query_embedding, 1)
        logger.debug(f'Closest document index: {indices[0][0]}')
        logger.debug(f'Closest document similarity: {scores[0][0]}')

        if scores[0][0] < settings.SIMILARITY_THRESHOLD:
            logger.info('No relevant context found.')
            return ''
        context = self.docs[indices[0][0]]
        logger.info(f'Retrieved context: {context}')
        return context

    def generate_answer(self, query: str, language: str = settings.LANGUAGE) -> str:
        context = self.retrieve_context(query)
        prompt = build_prompt(context, query, language)
        logger.debug('Generating answer with LLM...\n')
        return self.llm.generate(prompt)

