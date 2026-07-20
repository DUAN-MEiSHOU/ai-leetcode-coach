class LLMError(Exception):
    """Base class for LLM integration failures."""


class LLMConfigurationError(LLMError):
    """Raised when required provider configuration is missing."""


class LLMProviderError(LLMError):
    """Raised when the provider returns an unusable response."""
