from dataclasses import dataclass


@dataclass
class LLMModel:
    id: str
    name: str
    description: str
    llm_provider: str

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'llm_provider': self.llm_provider
        }


MODELS = [
    LLMModel(
        id='gpt-4o',
        name='GPT-4o',
        description='The full-size GPT-4o model.',
        llm_provider='openai',
    ),
    LLMModel(
        id='chatgpt-4o-latest',
        name='ChatGPT-4o (latest)',
        description='Latest used in ChatGPT',
        llm_provider='openai',
    ),
    LLMModel(
        id='gpt-4o-mini',
        name='GPT-4o Mini',
        description='A smaller version of GPT-4o.',
        llm_provider='openai',
    ),
    LLMModel(
        id='o1',
        name='O1',
        description='The O1 reasoning model.',
        llm_provider='openai',
    ),
    LLMModel(
        id='o1-mini',
        name='O1 Mini',
        description='A smaller version of the O1 model.',
        llm_provider='openai',
    ),
    LLMModel(
        id='o3-mini',
        name='O3 Mini',
        description='A smaller version of the O3 model.',
        llm_provider='openai',
    ),
    LLMModel(
        id="claude-3-5-sonnet-latest",
        name="Claude 3.5 Sonnet (latest)",
        description="Latest version of the Claude 3.5 Sonnet model.",
        llm_provider="anthropic",
    ),
    LLMModel(
        id="claude-3-5-haiku-latest",
        name="Claude 3.5 Haiku (latest)",
        description="Latest version of the Claude 3.5 Haiku model.",
        llm_provider="anthropic",
    )
]
