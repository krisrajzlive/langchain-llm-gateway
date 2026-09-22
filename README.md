# LangChain LLM Gateway

A small reference project demonstrating LangChain's "model gateway" pattern:
using `init_chat_model` and `Runnable` composition to treat different LLM
providers as interchangeable, resilient, and configurable at runtime — the
same responsibilities a dedicated LLM gateway/proxy would own.

## Features demonstrated

| # | Demo | Feature |
|---|------|---------|
| 1 | [`demos/demo_01_basic_gateway.py`](demos/demo_01_basic_gateway.py) | Provider-agnostic init via `init_chat_model("provider:model")` (OpenAI, Hugging Face, Ollama Cloud) |
| 2 | [`demos/demo_02_fallbacks.py`](demos/demo_02_fallbacks.py) | Automatic provider fallback with `with_fallbacks` (3-tier chain: OpenAI → Hugging Face → Ollama Cloud) |
| 3 | [`demos/demo_03_retry_and_rate_limit.py`](demos/demo_03_retry_and_rate_limit.py) | Retries (`with_retry`) and client-side rate limiting (`InMemoryRateLimiter`) |
| 4 | [`demos/demo_04_caching.py`](demos/demo_04_caching.py) | Response caching with `InMemoryCache`, with wire-level proof (real HTTP request count) that the cached call makes zero network calls |
| 5 | [`demos/demo_05_streaming.py`](demos/demo_05_streaming.py) | Token streaming, uniform across providers |
| 6 | [`demos/demo_06_structured_output.py`](demos/demo_06_structured_output.py) | Schema-constrained output with `with_structured_output` |
| 7 | [`demos/demo_07_tool_calling.py`](demos/demo_07_tool_calling.py) | Tool calling with `bind_tools` |
| 8 | [`demos/demo_08_configurable_alternatives.py`](demos/demo_08_configurable_alternatives.py) | Runtime-selectable model/params via `configurable_fields` / `configurable_alternatives` (OpenAI vs. Hugging Face) |
| 9 | [`demos/demo_09_huggingface_gateway.py`](demos/demo_09_huggingface_gateway.py) | Free hosted gateway: [Hugging Face Inference Providers](https://huggingface.co/docs/inference-providers) via an OpenAI-compatible endpoint |
| 10 | [`demos/demo_10_spend_limit.py`](demos/demo_10_spend_limit.py) | Spend limit: a budget cap enforced via a custom callback that prices token usage |
| 11 | [`demos/demo_11_call_rate_limits.py`](demos/demo_11_call_rate_limits.py) | Rate/call limits at the agent level via `ModelCallLimitMiddleware` |
| 12 | [`demos/demo_12_pii_data_policy.py`](demos/demo_12_pii_data_policy.py) | Data policy: PII detection with `redact`/`mask`/`block` strategies via `PIIMiddleware` |
| 13 | [`demos/demo_13_content_guardrail.py`](demos/demo_13_content_guardrail.py) | Guardrail: a custom `AgentMiddleware` that blocks disallowed topics before the model is ever called |
| 14 | [`demos/demo_14_reasoning_effort.py`](demos/demo_14_reasoning_effort.py) | Per-request effort tuning on a single model via `reasoning_effort` (`low`/`medium`/`high`) on `gpt-oss:20b` via Ollama Cloud |
| 15 | [`demos/demo_15_callbacks.py`](demos/demo_15_callbacks.py) | LangChain's callback lifecycle (`on_chat_model_start`, `on_llm_new_token`, `on_llm_end`, `on_tool_start`/`on_tool_end`, `on_chain_start`/`on_chain_end`) -- the hook point demo 10's spend limiter is secretly built on |

The `gateway/` package holds the shared `get_model()` helper (a thin wrapper
around `init_chat_model`) that every demo builds on.

Demos 10-13 cover the governance/operator side of a gateway (spend limits,
rate limits, data policy, guardrails), built on `langchain.agents` and
`langchain.agents.middleware`. 11 and 12 use official, built-in middleware
(`ModelCallLimitMiddleware`, `PIIMiddleware`); 10 and 13 show how to build a
custom callback/middleware for policies LangChain doesn't ship out of the
box (dollar-denominated budgets, arbitrary content guardrails).

Demo 14 is a different kind of lever from 1/2/8/9: those route a request
across *different* models/providers, while 14 tunes the *same* model's
reasoning depth per request via `reasoning_effort` -- the same idea behind
Claude Code's own model-effort picker.

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

# Hugging Face Inference Providers token (free tier) - used by demos 2, 8, 9
HUGGINGFACE_API_KEY=

# Ollama Cloud API key (free tier covers smaller models like gpt-oss:20b)
# used as the final fallback tier in demo 2
OLLAMA_API_KEY=

# Optional: only needed if you want to swap Hugging Face/Ollama back out
# for a paid Anthropic backend in demos 2/8
ANTHROPIC_API_KEY=

# Optional: enable LangSmith tracing for all demos
LANGSMITH_API_KEY=
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=langchain-llm-gateway
```

`OPENAI_API_KEY`, `HUGGINGFACE_API_KEY` (free — Settings → Access Tokens on
huggingface.co), and `OLLAMA_API_KEY` (free — Settings → API Keys on
ollama.com) are all you need to run every demo in this repo end to end; no
paid Anthropic key required. `ANTHROPIC_API_KEY` is unused by default —
it's only relevant if you edit demos 2/8 to route a branch through
Anthropic instead. If `LANGSMITH_API_KEY` is set, every demo's runs are
automatically traced to the `langchain-llm-gateway` project in LangSmith —
useful for inspecting fallbacks, retries, and tool-calling steps.

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
demos/            one script per gateway feature (demo_01 .. demo_13)
main.py           CLI menu to run any demo
requirements.txt  dependencies (installed via uv)
```

## Agent instructions

This repo includes [`AGENTS.md`](AGENTS.md) with conventions for AI coding
agents (package management, layout, coding conventions). [`CLAUDE.md`](CLAUDE.md)
imports `AGENTS.md` so Claude Code picks up the same instructions.
