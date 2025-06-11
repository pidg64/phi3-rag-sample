# app/services/llama_llm.py

from llama_cpp import Llama
from app.services.base_llm import BaseLLM
from app.core.settings import settings

class LlamaLLM(BaseLLM):
    def __init__(self):
        self.model = Llama(
            model_path=settings.MODEL_PATH,
            n_ctx=settings.N_CTX,
            n_threads=settings.N_THREADS,
            n_gpu_layers=settings.N_GPU_LAYERS,
            verbose=False
        )

    def generate(self, prompt: str) -> str:
        output = self.model(prompt, max_tokens=150, temperature=0.7, stop=["###"])
        return output["choices"][0]["text"].strip().split("\n")[0].strip()
