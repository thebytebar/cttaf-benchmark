"""
Model registry and provider configuration for CTTAF benchmark.

Defines all supported models and the API providers used to reach them.
Models that lack a confirmed public API endpoint are documented in
NO_PUBLIC_API (see bottom of file).

NOTE: Several model IDs in this registry are forward-looking (e.g. gpt-5.4,
gemini-3.1-pro, claude-sonnet-4-6) and reflect anticipated release names.
Update the "model_id" field to the exact identifier used by the provider's
API once the model is generally available.
"""

# ---------------------------------------------------------------------------
# Provider configurations
# ---------------------------------------------------------------------------
# Each provider entry contains:
#   base_url  – custom base URL for the OpenAI-compatible endpoint
#               (None → use default OpenAI endpoint)
#   env_key   – environment variable that holds the API key
#   description – human-readable label
# ---------------------------------------------------------------------------
PROVIDERS = {
    "openai": {
        "base_url": None,
        "env_key": "OPENAI_API_KEY",
        "description": "OpenAI API",
    },
    "anthropic": {
        # Uses the Anthropic Python SDK directly (not OpenAI-compatible)
        "env_key": "ANTHROPIC_API_KEY",
        "description": "Anthropic API (direct SDK)",
    },
    "google": {
        # Gemini models via Google's OpenAI-compatible endpoint
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "env_key": "GOOGLE_API_KEY",
        "description": "Google AI (Gemini / Gemma) via OpenAI-compatible endpoint",
    },
    "xai": {
        "base_url": "https://api.x.ai/v1",
        "env_key": "XAI_API_KEY",
        "description": "xAI (Grok) API",
    },
    "mistral": {
        "base_url": "https://api.mistral.ai/v1",
        "env_key": "MISTRAL_API_KEY",
        "description": "Mistral AI API (OpenAI-compatible)",
    },
    "deepseek": {
        "base_url": "https://api.deepseek.com",
        "env_key": "DEEPSEEK_API_KEY",
        "description": "DeepSeek API (OpenAI-compatible)",
    },
    "openrouter": {
        # Aggregator used for models without a dedicated hosted API
        # (Llama 4, Qwen, Phi-4, Gemma 3, etc.)
        "base_url": "https://openrouter.ai/api/v1",
        "env_key": "OPENROUTER_API_KEY",
        "description": "OpenRouter aggregator (many open-weight models)",
    },
    "moonshot": {
        # Moonshot AI (Kimi) — OpenAI-compatible
        "base_url": "https://api.moonshot.cn/v1",
        "env_key": "MOONSHOT_API_KEY",
        "description": "Moonshot AI (Kimi) API (OpenAI-compatible)",
    },
    "zhipu": {
        # Zhipu AI (GLM) — OpenAI-compatible v4 endpoint
        "base_url": "https://open.bigmodel.cn/api/paas/v4/",
        "env_key": "ZHIPU_API_KEY",
        "description": "Zhipu AI (GLM) API (OpenAI-compatible)",
    },
    "minimax": {
        "base_url": "https://api.minimax.chat/v1",
        "env_key": "MINIMAX_API_KEY",
        "description": "MiniMax API (OpenAI-compatible)",
    },
    "nvidia": {
        # NVIDIA NIM hosted inference
        "base_url": "https://integrate.api.nvidia.com/v1",
        "env_key": "NVIDIA_API_KEY",
        "description": "NVIDIA NIM API (OpenAI-compatible)",
    },
    "cohere": {
        # Cohere's OpenAI-compatible compatibility endpoint
        "base_url": "https://api.cohere.com/compatibility/v1",
        "env_key": "COHERE_API_KEY",
        "description": "Cohere API via OpenAI-compatible endpoint",
    },
    "together": {
        "base_url": "https://api.together.xyz/v1",
        "env_key": "TOGETHER_API_KEY",
        "description": "Together AI API (OpenAI-compatible)",
    },
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "env_key": "GROQ_API_KEY",
        "description": "Groq API (OpenAI-compatible)",
    },
}

# ---------------------------------------------------------------------------
# Model registry
# ---------------------------------------------------------------------------
# Keys are the benchmark model IDs passed via --model.
# Values carry:
#   provider  – key into PROVIDERS above
#   model_id  – exact model identifier sent to the API
# ---------------------------------------------------------------------------
MODEL_REGISTRY = {

    # ── OpenAI / GPT-5 series ──────────────────────────────────────────────
    # Dominant consumer and enterprise leader (~60%+ share, 500 M+ users).
    "gpt-5.4":        {"provider": "openai", "model_id": "gpt-5.4"},
    "gpt-5":          {"provider": "openai", "model_id": "gpt-5"},
    "gpt-4o":         {"provider": "openai", "model_id": "gpt-4o"},
    "gpt-4-turbo":    {"provider": "openai", "model_id": "gpt-4-turbo"},
    "o1":             {"provider": "openai", "model_id": "o1"},
    "o3":             {"provider": "openai", "model_id": "o3"},
    # gpt-oss: forward-looking placeholder for OpenAI open-weight variant
    "gpt-oss":        {"provider": "openai", "model_id": "gpt-oss"},

    # ── Google / Gemini 3.1 series ─────────────────────────────────────────
    # Strong #2 via Google ecosystem; broad consumer/enterprise use.
    "gemini-3.1-pro":   {"provider": "google", "model_id": "gemini-3.1-pro"},
    "gemini-3.1-flash": {"provider": "google", "model_id": "gemini-3.1-flash"},
    # Gemini 2.x — stable production IDs available today
    "gemini-2.0-flash": {"provider": "google", "model_id": "gemini-2.0-flash"},
    "gemini-1.5-pro":   {"provider": "google", "model_id": "gemini-1.5-pro"},
    # Gemma 3 — lightweight open option; routed via OpenRouter
    "gemma-3":          {"provider": "openrouter", "model_id": "google/gemma-3-27b-it"},

    # ── Anthropic / Claude Sonnet 4.6, Opus 4.6/4.7 ───────────────────────
    # High professional/enterprise adoption; coding, reasoning, reliability.
    "claude-sonnet-4-6":        {"provider": "anthropic", "model_id": "claude-sonnet-4-6"},
    "claude-opus-4-6":          {"provider": "anthropic", "model_id": "claude-opus-4-6"},
    "claude-opus-4-7":          {"provider": "anthropic", "model_id": "claude-opus-4-7"},
    # Stable production aliases
    "claude-3-5-sonnet-latest": {"provider": "anthropic", "model_id": "claude-3-5-sonnet-latest"},
    "claude-3-opus-latest":     {"provider": "anthropic", "model_id": "claude-3-opus-latest"},

    # ── Meta / Llama 4 family ──────────────────────────────────────────────
    # Leading open-weight model; self-hosted + cloud (Groq, Together AI, etc.).
    # No direct Meta-hosted public API → routed via OpenRouter / Together / Groq.
    "llama-4-maverick":              {"provider": "openrouter", "model_id": "meta-llama/llama-4-maverick"},
    "llama-4-scout":                 {"provider": "openrouter", "model_id": "meta-llama/llama-4-scout"},
    "llama-4-maverick-together":     {"provider": "together",   "model_id": "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8"},
    "llama-4-scout-together":        {"provider": "together",   "model_id": "meta-llama/Llama-4-Scout-17B-16E-Instruct"},
    "llama-4-scout-groq":            {"provider": "groq",       "model_id": "llama-4-scout-17b-16e-instruct"},

    # ── xAI / Grok 4 ──────────────────────────────────────────────────────
    # Growing rapidly for real-time and uncensored use cases.
    "grok-4":   {"provider": "xai", "model_id": "grok-4"},
    "grok-4.1": {"provider": "xai", "model_id": "grok-4.1"},
    # Stable production alias
    "grok-3":   {"provider": "xai", "model_id": "grok-3"},

    # ── Mistral AI ─────────────────────────────────────────────────────────
    # Popular European option; strong developer and enterprise adoption.
    "mistral-large":      {"provider": "mistral", "model_id": "mistral-large-latest"},
    "mistral-large-2411": {"provider": "mistral", "model_id": "mistral-large-2411"},
    "mistral-medium":     {"provider": "mistral", "model_id": "mistral-medium-latest"},
    "mistral-small":      {"provider": "mistral", "model_id": "mistral-small-latest"},

    # ── DeepSeek V3.2 / R1 ────────────────────────────────────────────────
    # High API/token usage (especially on OpenRouter); strong open-weight adoption.
    "deepseek-v3.2": {"provider": "deepseek", "model_id": "deepseek-v3.2"},
    "deepseek-v3":   {"provider": "deepseek", "model_id": "deepseek-chat"},
    "deepseek-r1":   {"provider": "deepseek", "model_id": "deepseek-r1"},

    # ── Alibaba / Qwen 3.6 ────────────────────────────────────────────────
    # Massive in cost-sensitive/high-volume workflows; heavy Asian/global API use.
    # Qwen models are accessible via OpenRouter or DashScope (Alibaba Cloud).
    "qwen-3.6":       {"provider": "openrouter", "model_id": "qwen/qwen3-235b-a22b"},
    "qwen-max":       {"provider": "openrouter", "model_id": "qwen/qwen-max"},
    "qwen-plus":      {"provider": "openrouter", "model_id": "qwen/qwen-plus"},
    "qwen-coder-32b": {"provider": "openrouter", "model_id": "qwen/qwen-2.5-coder-32b-instruct"},

    # ── Moonshot AI / Kimi K2.6 ───────────────────────────────────────────
    # Strong aggregator and developer adoption, especially for coding/agent tasks.
    "kimi-k2.6":   {"provider": "moonshot", "model_id": "kimi-k2.6"},
    "moonshot-v1": {"provider": "moonshot", "model_id": "moonshot-v1-8k"},

    # ── Zhipu AI / GLM-5 ──────────────────────────────────────────────────
    # High token/API share, particularly in Asia and scientific/enterprise workflows.
    "glm-5": {"provider": "zhipu", "model_id": "glm-5"},
    "glm-4": {"provider": "zhipu", "model_id": "glm-4"},

    # ── MiniMax M2.5 / M2.7 ───────────────────────────────────────────────
    # Very high volume on OpenRouter and similar platforms.
    "minimax-m2.5": {"provider": "minimax", "model_id": "minimax-m2.5"},
    "minimax-m2.7": {"provider": "minimax", "model_id": "minimax-m2.7"},

    # ── NVIDIA / Nemotron 3 ───────────────────────────────────────────────
    # Popular in enterprise and free-tier / OpenRouter deployments.
    "nemotron-3":    {"provider": "nvidia", "model_id": "nvidia/llama-3.1-nemotron-70b-instruct"},
    "nemotron-3-8b": {"provider": "nvidia", "model_id": "nvidia/llama-3.1-nemotron-nano-8b-v1"},

    # ── Cohere / Command R+ ───────────────────────────────────────────────
    # Solid enterprise-focused API adoption.
    "command-r-plus": {"provider": "cohere", "model_id": "command-r-plus"},
    "command-r":      {"provider": "cohere", "model_id": "command-r"},

    # ── Microsoft / Phi-4 ─────────────────────────────────────────────────
    # Strong on-device/Azure integration; routed via OpenRouter for simplicity.
    "phi-4":         {"provider": "openrouter", "model_id": "microsoft/phi-4"},
    "phi-4-mini":    {"provider": "openrouter", "model_id": "microsoft/phi-4-mini"},
    "phi-4-multimodal": {"provider": "openrouter", "model_id": "microsoft/phi-4-multimodal-instruct"},

    # ── Specialized hybrids / derivatives ─────────────────────────────────
    # Broad developer and proxy API usage via Groq / Together AI.
    "llama-3.3-70b-groq":       {"provider": "groq",    "model_id": "llama-3.3-70b-versatile"},
    "llama-3.1-405b-together":  {"provider": "together", "model_id": "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo"},
    "deepseek-r1-together":     {"provider": "together", "model_id": "deepseek-ai/DeepSeek-R1"},
    "qwen-coder-together":      {"provider": "together", "model_id": "Qwen/Qwen2.5-Coder-32B-Instruct"},
}

# ---------------------------------------------------------------------------
# Models without confirmed public API access
# ---------------------------------------------------------------------------
# These models are noted here so the evaluator can surface a clear message
# rather than silently failing with an unknown API error.
# ---------------------------------------------------------------------------
NO_PUBLIC_API = {
    "mimo-v2-pro": (
        "MiMo-V2-Pro (Xiaomi) — No confirmed public API access. "
        "MiMo models are primarily open-weight (available on Hugging Face for "
        "self-hosting); Xiaomi has not announced a public hosted API endpoint."
    ),
    "hy3-preview": (
        "Hy3 Preview (Tencent) — No confirmed public API access. "
        "Tencent has not published a public API endpoint for Hy3 as of this writing. "
        "It may become available via Tencent Cloud in the future."
    ),
    "muse-spark": (
        "Muse Spark (Meta) — No confirmed public API access. "
        "Meta has not announced a public hosted API for Muse Spark. "
        "It may be accessible indirectly once listed on OpenRouter or Together AI."
    ),
}


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def get_model_info(model: str):
    """
    Return (provider_name, api_model_id) for the given benchmark model ID.

    If the model is not in MODEL_REGISTRY, the provider is auto-detected from
    common name prefixes and the raw model string is used as the API model ID.

    Returns (None, None) if the model is listed in NO_PUBLIC_API.
    """
    if model in NO_PUBLIC_API:
        return None, None

    if model in MODEL_REGISTRY:
        entry = MODEL_REGISTRY[model]
        return entry["provider"], entry["model_id"]

    # Fallback: heuristic detection so callers can pass raw API model names
    provider = _detect_provider_from_name(model)
    return provider, model


def list_models():
    """Return a sorted list of all registered benchmark model IDs."""
    return sorted(MODEL_REGISTRY.keys())


def _detect_provider_from_name(model: str) -> str:
    """Heuristically map a raw model name to a provider key."""
    name = model.lower()
    if name.startswith(("gpt-", "o1", "o3", "text-davinci")):
        return "openai"
    if name.startswith("claude-"):
        return "anthropic"
    if name.startswith(("gemini-", "gemma-")):
        return "google"
    if name.startswith("grok-"):
        return "xai"
    if name.startswith(("mistral-", "mixtral-")):
        return "mistral"
    if name.startswith("deepseek-"):
        return "deepseek"
    if name.startswith(("kimi-", "moonshot-")):
        return "moonshot"
    if name.startswith("glm-"):
        return "zhipu"
    if name.startswith("minimax-"):
        return "minimax"
    if name.startswith(("nemotron-", "nvidia/")):
        return "nvidia"
    if name.startswith("command-"):
        return "cohere"
    if name.startswith(("phi-", "microsoft/")):
        return "openrouter"
    if name.startswith(("llama-", "meta-llama/")):
        return "openrouter"
    if name.startswith(("qwen", "alibaba/")):
        return "openrouter"
    # Default: OpenRouter acts as a catch-all aggregator
    return "openrouter"
