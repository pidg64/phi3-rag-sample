from fastapi import FastAPI
from app.api.routes import router
from app.core.logger import setup_logger

logger = setup_logger()

app = FastAPI(
    title='RAG API',
    description='API para preguntas y respuestas con recuperación aumentada por contexto.',
    version='1.0.0',
)

app.include_router(router, prefix='/rag')

logger.info('FastAPI inicializada y lista.')


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        'run_api:app',
        host='0.0.0.0',
        port=8000,
        log_level='info'
    )