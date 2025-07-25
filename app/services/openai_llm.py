from app.services.base_llm import BaseLLM
from app.services.openai_service import OpenAIService


class OpenAILLM(BaseLLM):
    def __init__(self):
        self.service = OpenAIService()

    def generate(self, prompt: str) -> str:
        return self.service.generate(prompt)