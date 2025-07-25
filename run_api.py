from fastapi import FastAPI
from app.api.routes import router
from app.core.logger import logger

app = FastAPI(
    title='RAG API',
    description='API para preguntas y respuestas con recuperación aumentada por contexto.',
    version='1.0.0',
)

app.include_router(router, prefix='/rag')


if __name__ == '__main__':
    import uvicorn
    logger.info('Starting the RAG API service...')
    uvicorn.run(
        'run_api:app',
        host='0.0.0.0',
        port=8000,
        log_level='info'
    )