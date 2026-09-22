"""Thin wrapper around LangChain's model gateway (`init_chat_model`).

`init_chat_model` is LangChain's provider-agnostic entry point: pass a
"provider:model" string (or a bare model name plus `model_provider`) and get
back a `BaseChatModel` with a uniform interface, regardless of which vendor
SDK sits underneath. That uniformity is what makes the rest of the demos in
this repo (fallbacks, retries, streaming, structured output, tool calling)
work identically across providers.
"""

from __future__ import annotations

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel

load_dotenv()

DEFAULT_MODEL = "openai:gpt-4o-mini"
FALLBACK_MODEL = "anthropic:claude-3-5-haiku-latest"


def get_model(model: str = DEFAULT_MODEL, **kwargs) -> BaseChatModel:
    """Return a chat model instance for the given "provider:model" string."""
    return init_chat_model(model, **kwargs)
