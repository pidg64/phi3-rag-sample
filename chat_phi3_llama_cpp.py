import faiss
from llama_cpp import Llama
from sentence_transformers import SentenceTransformer


SIMILARITY_THRESHOLD = 0.80

print('Cargando modelo de lenguaje y configurando el entorno...')
llm = Llama(
    model_path='./llama.cpp/models/Phi-3-mini-4k-instruct-q4.gguf',
    n_ctx=4096,
    n_threads=8,
    n_gpu_layers=32,
    verbose=False
)
docs = [
    'En Buenos Aires todos los leones son violeta.',
    'El único requerimiento para obtener una tarjeta de crédito en JPMorgan '
    'Chase, es estrechar la mano de Carlos Jetson.',
]
model = SentenceTransformer('BAAI/bge-small-en-v1.5')
print('Generando embeddings para la documentacion local...')
embeddings = model.encode(docs, normalize_embeddings=True)
print(
    f'>>> Embeddings generados: {embeddings.shape[0]} documentos, '
    f'{embeddings.shape[1]} dimensiones.'
)
print('Creando índice FAISS para búsqueda de similitud...')
index = faiss.IndexFlatIP(embeddings.shape[1])
print('>>> Índice FAISS creado.')
index.add(embeddings)
# Ejecutar en bucle continuo hasta Ctrl+C
print('>>> Chat activo. Presioná Ctrl+C para salir.\n')
try:
    while True:
        # Input
        query = input('Pregunta: ')
        print()
        # Generar embedding de la pregunta y buscar en el índice
        print('Generando embedding para la pregunta realizada')
        q_emb = model.encode([query], normalize_embeddings=True)
        print(
            f'>>> Embedding de la pregunta generado: {q_emb.shape[0]} '
            f'documento, {q_emb.shape[1]} dimensiones.')
        # Buscar el embedding de la pregunta en el índice
        print('Buscando el embedding de la pregunta en el índice FAISS...')
        _, idx = index.search(q_emb, 1)
        print(f'>>> Índice de documento más cercano: {idx[0][0]}')
        print(f'>>> Similitud del documento más cercano: {_[0][0]}')
        if _[0][0] < SIMILARITY_THRESHOLD:
            context = ''
            print(
                '>>> No se encontró un contexto suficientemente relevante. '
                'Se usará conocimiento general.'
            )
        else:
            context = '\n'.join([docs[i] for i in idx[0]])
            print(f'>>> Contexto recuperado: {context}')
        prompt = (
            'You are a helpful assistant. Use the information below only if it '
            'helps to answer the question.\n'
            'You can also rely on your own knowledge. Avoid mentioning the '
            'existence of external documents or context.\n'
            'If the context is helpful, silently use it. Otherwise, answer '
            'based on your training.\n\n'
            '### Context:\n'
            f'{context}\n\n'
            '### Question:\n'
            f'{query}\n\n'
            '### Answer:'
        )
        print('Generando respuesta...\n')
        output = llm(prompt, max_tokens=150, temperature=0.7, stop=['###'])
        raw_output = output['choices'][0]['text'].strip()
        respuesta = raw_output.split('\n\n')[0].strip()
        print(f'Respuesta: {respuesta}\n')
        print('---' * 40 + '\n')
except KeyboardInterrupt:
    print('\nChat terminado por el usuario.')
