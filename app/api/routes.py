# app/api/routes.py

from fastapi import APIRouter, Depends
from app.services.rag import RAGService
from app.api.deps import get_rag_service
from app.schemas.rag import QueryRequest, QueryResponse

router = APIRouter()

@router.post('/ask', response_model=QueryResponse)
def ask_question(
    payload: QueryRequest,
    rag_service: RAGService = Depends(get_rag_service)
):
    answer = rag_service.generate_answer(payload.question, payload.language)
    return QueryResponse(answer=answer)
