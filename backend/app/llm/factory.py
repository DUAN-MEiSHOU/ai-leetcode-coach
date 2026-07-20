from app.core.config import get_settings
from app.llm.provider import LLMProvider
from app.llm.providers.deepseek import DeepSeekProvider


def create_llm_provider() -> LLMProvider:
    return DeepSeekProvider(get_settings())
