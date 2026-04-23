"""
Provider routing for CTTAF benchmark model evaluation.

Routes target-model queries to the appropriate API based on the model
registry in models_config.py.  Two SDKs are used:

  • openai  – for all OpenAI-compatible providers (OpenAI, Google, xAI,
              Mistral, DeepSeek, OpenRouter, Moonshot, Zhipu, MiniMax,
              NVIDIA, Cohere, Together AI, Groq, …)
  • anthropic – for Anthropic models (Claude family)

Clients are created on first use and cached for the lifetime of the process
to avoid redundant connection setup.
"""

import logging
import os
import sys
from typing import Optional

logger = logging.getLogger(__name__)

# Lazy client cache keyed by a provider identifier string
_client_cache: dict = {}

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
# Temperature 0.7 is used for target-model queries to match the original
# benchmark design.  Judges always use temperature 0.0 (set in evaluate_model.py).
_TARGET_TEMPERATURE = 0.7
_TARGET_MAX_TOKENS = 500


def get_model_response(model: str, question: str) -> str:
    """
    Query *model* with *question* and return its text response.

    Args:
        model:    Benchmark model ID (a key in MODEL_REGISTRY, or a raw
                  API model name for auto-detected providers).
        question: The question text to send to the model.

    Returns:
        The model's text response as a string.

    Raises:
        ValueError:   If the model is listed in NO_PUBLIC_API.
        RuntimeError: If the required API key environment variable is not set.
        Exception:    Propagates any API-level error to the caller.
    """
    from models_config import get_model_info, NO_PUBLIC_API, PROVIDERS

    if model in NO_PUBLIC_API:
        raise ValueError(
            f"Cannot evaluate '{model}': {NO_PUBLIC_API[model]}"
        )

    provider, api_model_id = get_model_info(model)

    if provider is None:
        raise ValueError(f"Unknown model '{model}' and no provider could be detected.")

    if provider not in PROVIDERS:
        raise ValueError(f"Provider '{provider}' is not configured in PROVIDERS.")

    provider_config = PROVIDERS[provider]
    api_key = os.getenv(provider_config["env_key"])

    if not api_key:
        raise RuntimeError(
            f"Missing API key for provider '{provider}' "
            f"(model: '{model}'). "
            f"Set {provider_config['env_key']} in your .env file."
        )

    if provider == "anthropic":
        return _call_anthropic(api_key, api_model_id, question)

    return _call_openai_compatible(
        api_key=api_key,
        base_url=provider_config.get("base_url"),
        model_id=api_model_id,
        question=question,
        provider=provider,
    )


def validate_model_api_key(model: str) -> bool:
    """
    Check that the API key required for *model* is present in the environment.

    Returns True if the key exists, False (with a logged warning) if not.
    Does not raise; intended as an early-startup sanity check.
    """
    from models_config import get_model_info, NO_PUBLIC_API, PROVIDERS

    if model in NO_PUBLIC_API:
        logger.error(
            "Model '%s' has no public API: %s", model, NO_PUBLIC_API[model]
        )
        return False

    provider, _ = get_model_info(model)
    if provider is None:
        logger.error("Could not determine a provider for model '%s'.", model)
        return False

    provider_config = PROVIDERS.get(provider, {})
    env_key = provider_config.get("env_key", "")

    if not os.getenv(env_key):
        logger.warning(
            "API key '%s' is not set for model '%s' (provider: %s). "
            "Evaluation will fail when the model is queried.",
            env_key, model, provider,
        )
        return False

    return True


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _call_openai_compatible(
    api_key: str,
    base_url: Optional[str],
    model_id: str,
    question: str,
    provider: str,
) -> str:
    """Call any OpenAI-compatible API endpoint."""
    try:
        from openai import OpenAI
    except ImportError:
        logger.error("openai package is not installed. Run: pip install openai")
        sys.exit(1)

    cache_key = f"openai:{base_url}"
    if cache_key not in _client_cache:
        kwargs = {"api_key": api_key}
        if base_url:
            kwargs["base_url"] = base_url
        _client_cache[cache_key] = OpenAI(**kwargs)

    client = _client_cache[cache_key]
    response = client.chat.completions.create(
        model=model_id,
        messages=[{"role": "user", "content": question}],
        temperature=_TARGET_TEMPERATURE,
        max_tokens=_TARGET_MAX_TOKENS,
    )
    return response.choices[0].message.content


def _call_anthropic(api_key: str, model_id: str, question: str) -> str:
    """Call the Anthropic Messages API."""
    try:
        from anthropic import Anthropic
    except ImportError:
        logger.error("anthropic package is not installed. Run: pip install anthropic")
        sys.exit(1)

    if "anthropic" not in _client_cache:
        _client_cache["anthropic"] = Anthropic(api_key=api_key)

    client = _client_cache["anthropic"]
    response = client.messages.create(
        model=model_id,
        max_tokens=_TARGET_MAX_TOKENS,
        messages=[{"role": "user", "content": question}],
    )
    return response.content[0].text
