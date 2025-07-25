# main.py

from app.cli.chat import chat_loop
from app.services.rag import RAGService
from app.core.logger import logger

logger.info('Starting the RAG Chat service...')
rag_service = RAGService()
chat_loop(rag_service)
