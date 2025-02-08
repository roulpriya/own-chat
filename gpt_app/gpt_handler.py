import os
from dataclasses import dataclass

import requests


@dataclass
class Message:
    role: str
    content: str


class LLMHandler:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    def generate_response(self, model_name, system_message: str, messages: list[Message] = None) -> str:
        return self._call_openai_api(model_name, system_message, messages)

    def _call_openai_api(self, model_name: str, message: str, messages: list[Message]) -> str:
        """Handle OpenAI API calls
        :param messages:
        """
        headers = {
            'Authorization': f"Bearer {self.base_url}",
            'Content-Type': 'application/json'
        }

        payload = {
            'model': model_name,
            'messages': [{'role': 'user', 'content': message}],
            'temperature': 0.7
        }

        response = requests.post(
            f'{self.base_url}/chat/completions',
            headers=headers,
            json=payload
        )

        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']


_llm_handlers = {}


def _create_llm_handler(provider: str):
    if provider == 'openai':
        return LLMHandler(
            base_url='https://api.openai.com/v1',
            api_key=os.getenv(f'{provider}_API_KEY')
        )

    raise ValueError(f'Unknown LLM provider: {provider}')


def get_llm_handler(provider: str) -> LLMHandler:
    if provider not in _llm_handlers:
        _llm_handlers[provider] = _create_llm_handler(provider)

    return _llm_handlers[provider]
