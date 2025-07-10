def build_prompt(context: str, query: str, language: str = 'es') -> str:
    if language == 'en':
        system_prompt = (
            'You are a helpful assistant. Use the information below only if it '
            'helps to answer the question.\n'
            'You can also rely on your own knowledge. Avoid mentioning the '
            'existence of external documents or context.\n'
            'If the context is helpful, silently use it. Otherwise, answer '
            'based on your training.\n\n'
        )
        question_header = '### Question:'
        answer_header = '### Answer:'
        context_header = '### Context:'
    elif language == 'es':
        system_prompt = (
            'Sos un asistente útil. Usá la información a continuación solo si sirve '
            'para responder la pregunta.\n'
            'También podés basarte en tu conocimiento general. Evitá mencionar que '
            'la información proviene de un documento externo o contexto.\n'
            'Si el contexto es útil, usalo silenciosamente. Si no lo es, respondé '
            'en base a tu entrenamiento.\n\n'
        )
        question_header = '### Pregunta:'
        answer_header = '### Respuesta:'
        context_header = '### Contexto:'
    else:
        raise ValueError(f'Idioma no soportado: {language}')

    return (
        f'{system_prompt}'
        f'{context_header}\n'
        f'{context}\n\n'
        f'{question_header}\n'
        f'{query}\n\n'
        f'{answer_header}'
    )