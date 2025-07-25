# app/services/openai.py

from openai import OpenAI
from app.core.settings import settings
from app.core.logger import setup_logger

logger = setup_logger()


class OpenAIService:
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY no configurada en las variables de entorno.")
        
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL_NAME
        self.temperature = settings.OPENAI_TEMPERATURE
        logger.debug("Servicio de OpenAI inicializado.")

    def generate(self, prompt: str) -> str:
        logger.debug(f"Enviando prompt a OpenAI: {prompt}")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
            )
            
            if response.choices:
                content = response.choices[0].message.content.strip()
                logger.debug(f"Respuesta de OpenAI recibida: {content}")
                return content
            else:
                logger.error("La respuesta de OpenAI no contiene 'choices'.")
                raise ValueError("Respuesta inválida de la API de OpenAI")

        except Exception as e:
            logger.error(f"Error en la llamada a la API de OpenAI: {e}")
            raise
