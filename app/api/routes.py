# app/api/routes.py

import time
from fastapi import APIRouter, Depends
from app.services.rag import RAGService
from app.api.deps import get_rag_service
from app.schemas.rag import QueryRequest, QueryResponse
from app.core.logger import logger

router = APIRouter()


@router.post('/ask', response_model=QueryResponse)
def ask_question(
    payload: QueryRequest,
    rag_service: RAGService = Depends(get_rag_service)
):
    start_time = time.time()
    answer = rag_service.generate_answer(payload.question, payload.language)
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(f'Response generation took {elapsed_time:.2f} seconds.')
    return QueryResponse(answer=answer)
