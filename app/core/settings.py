# settings.py

import os

class Settings:
    DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1']
    LANGUAGE = os.getenv('LANGUAGE', 'en').lower()
    
    try:
        SIMILARITY_THRESHOLD = float(os.getenv('SIMILARITY_THRESHOLD', '0.80'))
    except ValueError:
        SIMILARITY_THRESHOLD = 0.80  # Fallback seguro

    MODEL_PATH = os.getenv('MODEL_PATH', './models/Phi-3-mini-4k-instruct-q4.gguf')
    EMBEDDING_MODEL_NAME = os.getenv('EMBEDDING_MODEL_NAME', 'intfloat/multilingual-e5-small')
    EMBEDDING_MODEL_PATH = os.getenv('EMBEDDING_MODEL_PATH', './models/local-multilingual-e5-small')
    DOCS_PATH = os.getenv('DOCS_PATH', './docs/local_kb_es.txt')
    LLM_BACKEND: str = os.getenv('LLM_BACKEND', 'llama')  # o 'ollama'
    
    # Recursos para llama-cpp
    N_CTX = int(os.getenv('N_CTX', '4096'))
    N_THREADS = int(os.getenv('N_THREADS', '8'))
    N_GPU_LAYERS = int(os.getenv('N_GPU_LAYERS', '32'))

    # Configuracion de OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL_NAME = os.getenv('OPENAI_MODEL_NAME', 'gpt-3.5-turbo')
    try:
        OPENAI_TEMPERATURE = float(os.getenv('OPENAI_TEMPERATURE', '0.7'))
    except ValueError:
        OPENAI_TEMPERATURE = 0.7


settings = Settings()
