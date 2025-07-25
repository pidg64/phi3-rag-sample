# app/services/ollama_llm.py

from app.services.base_llm import BaseLLM
from app.services.ollama_service import OllamaService

class OllamaLLM(BaseLLM):
    def __init__(self):
        self.client = OllamaService()

    def generate(self, prompt: str) -> str:
        return self.client.generate(prompt)
