"""Chat model factory.

Only Gemini is implemented. Additional providers (for example Groq)
can be added as further branches in ``get_llm``.
"""

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI

from core.config import Settings, get_settings


def get_llm(settings: Settings | None = None) -> BaseChatModel:
    """Return a chat model for the configured provider."""
    resolved = settings if settings is not None else get_settings()
    provider = resolved.llm_provider.strip().lower()

    if provider == "gemini":
        if not resolved.google_api_key:
            msg = "GOOGLE_API_KEY is not set"
            raise ValueError(msg)
        if not resolved.gemini_model:
            msg = "GEMINI_MODEL is not set"
            raise ValueError(msg)
        return ChatGoogleGenerativeAI(
            model=resolved.gemini_model,
            google_api_key=resolved.google_api_key,
        )

    msg = f"Unsupported LLM provider: {resolved.llm_provider}"
    raise ValueError(msg)
