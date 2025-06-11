from app.services.rag import RAGService

# Esto evita que se inicialice en cada request
rag_service_instance = RAGService()

def get_rag_service() -> RAGService:
    return rag_service_instance
