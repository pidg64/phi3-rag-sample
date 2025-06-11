# app/cli/chat.py

from app.core.logger import setup_logger

logger = setup_logger()

def chat_loop(rag_service):
    logger.info('>>> Chat activo. Presioná Ctrl+C para salir.\n')
    try:
        while True:
            user_input = input('Pregunta: ')
            logger.info('')
            respuesta = rag_service.generate_answer(user_input)
            print(f'Respuesta: {respuesta}\n')
            print('---' * 40 + '\n')
    except KeyboardInterrupt:
        logger.debug('\nChat terminado por el usuario.')
