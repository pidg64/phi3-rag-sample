from pydantic import BaseModel, Field
from typing import Literal

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1)
    language: Literal['es', 'en'] = 'es'

class QueryResponse(BaseModel):
    answer: str
