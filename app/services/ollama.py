# app/services/ollama.py

import base64
import requests

from pathlib import Path
from typing import Optional


class OllamaService:
    def __init__(self, model: str = 'qwen2:vl', host: str = 'http://localhost', port: int = 11434):
        self.base_url = f'{host}:{port}'
        self.model = model
        self.api_url = f'{self.base_url}/api/generate'

    def _encode_image(self, image_path: Path) -> str:
        with open(image_path, 'rb') as f:
            encoded = base64.b64encode(f.read()).decode('utf-8')
        return f'data:image/jpeg;base64,{encoded}'

    def generate(
        self,
        prompt: str,
        image_path: Optional[str] = None,
        stream: bool = False
    ) -> str:
        payload = {
            'model': self.model,
            'prompt': prompt,
            'stream': stream
        }

        if image_path:
            image_encoded = self._encode_image(Path(image_path))
            payload['images'] = [image_encoded]

        response = requests.post(self.api_url, json=payload)
        response.raise_for_status()

        return response.json()['response']
