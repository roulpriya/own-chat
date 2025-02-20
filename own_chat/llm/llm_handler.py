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

    def generate_response(
        self, model_name: str, system_message: str, messages: list[Message] = None
    ) -> str:
        return self._call_openai_api(model_name, system_message, messages)

    def _call_openai_api(
        self, model_name: str, message: str, messages: list[Message]
    ) -> str:
        """Handle OpenAI API calls
        :param messages:
        """
        headers = {
            "Authorization": f"Bearer {self.base_url}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": message}],
            "temperature": 0.7,
        }

        response = requests.post(
            f"{self.base_url}/chat/completions", headers=headers, json=payload
        )

        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
