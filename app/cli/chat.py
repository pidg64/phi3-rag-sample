# app/cli/chat.py

from app.core.logger import logger

def chat_loop(rag_service):
    logger.info('>>> Chat active. Press Ctrl+C to exit.\n')
    try:
        while True:
            user_input = input('Pregunta: ')
            logger.info('')
            respuesta = rag_service.generate_answer(user_input)
            print(f'Response: {respuesta}\n')
            print('---' * 40 + '\n')
    except KeyboardInterrupt:
        logger.debug('\nChat ended by user.')
