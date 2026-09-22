# LangChain LLM Gateway

A small reference project demonstrating LangChain's "model gateway" pattern:
using `init_chat_model` and `Runnable` composition to treat different LLM
providers as interchangeable, resilient, and configurable at runtime — the
same responsibilities a dedicated LLM gateway/proxy would own.

## Features demonstrated

| # | Demo | Feature |
|---|------|---------|
| 1 | [`demos/demo_01_basic_gateway.py`](demos/demo_01_basic_gateway.py) | Provider-agnostic init via `init_chat_model("provider:model")` |
| 2 | [`demos/demo_02_fallbacks.py`](demos/demo_02_fallbacks.py) | Automatic provider fallback with `with_fallbacks` |
| 3 | [`demos/demo_03_retry_and_rate_limit.py`](demos/demo_03_retry_and_rate_limit.py) | Retries (`with_retry`) and client-side rate limiting (`InMemoryRateLimiter`) |
| 4 | [`demos/demo_04_caching.py`](demos/demo_04_caching.py) | Response caching with `InMemoryCache` |
| 5 | [`demos/demo_05_streaming.py`](demos/demo_05_streaming.py) | Token streaming, uniform across providers |
| 6 | [`demos/demo_06_structured_output.py`](demos/demo_06_structured_output.py) | Schema-constrained output with `with_structured_output` |
| 7 | [`demos/demo_07_tool_calling.py`](demos/demo_07_tool_calling.py) | Tool calling with `bind_tools` |
| 8 | [`demos/demo_08_configurable_alternatives.py`](demos/demo_08_configurable_alternatives.py) | Runtime-selectable model/params via `configurable_fields` / `configurable_alternatives` |
| 9 | [`demos/demo_09_huggingface_gateway.py`](demos/demo_09_huggingface_gateway.py) | Free hosted gateway: [Hugging Face Inference Providers](https://huggingface.co/docs/inference-providers) via an OpenAI-compatible endpoint |

The `gateway/` package holds the shared `get_model()` helper (a thin wrapper
around `init_chat_model`) that every demo builds on.

## Setup

This project uses **uv** for package management (`requirements.txt`, not
`pyproject.toml`).

```bash
uv venv
uv pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in the provider keys you want to use:

```bash
cp .env.example .env
```

```
OPENAI_API_KEY=
ANTHROPIC_API_KEY=

# Hugging Face Inference Providers token (free tier) - used by demo 9
HUGGINGFACE_API_KEY=

# Optional: enable LangSmith tracing for all demos
LANGSMITH_API_KEY=
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=langchain-llm-gateway
```

`ANTHROPIC_API_KEY` is only needed for demos that touch Anthropic models
(2 and 8's alternative branch); the rest run on OpenAI alone.
`HUGGINGFACE_API_KEY` (a free Hugging Face access token — Settings → Access
Tokens on huggingface.co) is only needed for demo 9, which runs against the
free, OpenAI-compatible [Hugging Face Inference Providers](https://huggingface.co/docs/inference-providers)
gateway instead of a paid provider. If `LANGSMITH_API_KEY` is set, every
demo's runs are automatically traced to the `langchain-llm-gateway` project
in LangSmith — useful for inspecting fallbacks, retries, and tool-calling
steps.

## Running the demos

Interactive menu:

```bash
python main.py
```

Or run a specific demo directly:

```bash
python main.py 4        # runs demo 4 (caching)
python demos/demo_05_streaming.py
```

## Repository layout

```
gateway/          shared init_chat_model wrapper
demos/            one script per gateway feature (demo_01 .. demo_08)
main.py           CLI menu to run any demo
requirements.txt  dependencies (installed via uv)
```

## Agent instructions

This repo includes [`AGENTS.md`](AGENTS.md) with conventions for AI coding
agents (package management, layout, coding conventions). [`CLAUDE.md`](CLAUDE.md)
imports `AGENTS.md` so Claude Code picks up the same instructions.
