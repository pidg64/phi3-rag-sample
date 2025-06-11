# main.py

from app.cli.chat import chat_loop
from app.services.rag import RAGService
from app.core.logger import setup_logger

setup_logger()
rag_service = RAGService()
chat_loop(rag_service)
