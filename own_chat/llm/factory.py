import os

from own_chat.llm.llm_handler import LLMHandler

_llm_handlers = {}


def _create_llm_handler(provider: str):
    if provider == "openai":
        return LLMHandler(
            base_url="https://api.openai.com/v1",
            api_key=os.getenv(f"{provider}_API_KEY"),
        )

    raise ValueError(f"Unknown LLM provider: {provider}")


def get_llm_handler(provider: str) -> LLMHandler:
    if provider not in _llm_handlers:
        _llm_handlers[provider] = _create_llm_handler(provider)

    return _llm_handlers[provider]
