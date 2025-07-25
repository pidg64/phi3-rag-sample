from typing import Literal

from app.core.settings import settings
from pydantic import BaseModel, Field, field_validator

ALLOWED_LANGUAGES = ('es', 'en')


def get_default_language() -> Literal['es', 'en']:
    if settings.LANGUAGE not in ALLOWED_LANGUAGES:
        raise ValueError(f"LANGUAGE setting must be one of {ALLOWED_LANGUAGES}")
    return settings.LANGUAGE  # type: ignore


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1)
    language: Literal['es', 'en'] = Field(
        default_factory=get_default_language,
        examples=['en']
    )

    @field_validator('language')
    @classmethod
    def validate_language(cls, v: str) -> str:
        if v not in ALLOWED_LANGUAGES:
            raise ValueError(f'language must be one of {ALLOWED_LANGUAGES}')
        return v


class QueryResponse(BaseModel):
    answer: str