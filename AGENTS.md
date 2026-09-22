# AGENTS.md

Instructions for AI coding agents (Claude Code, Codex, etc.) working in this repository.

## Project purpose

This repo demonstrates LangChain's model-gateway pattern: using
`init_chat_model` and related `Runnable` composition primitives
(`with_fallbacks`, `with_retry`, rate limiting, caching, `bind_tools`,
`with_structured_output`, `configurable_alternatives`) to treat multiple LLM
providers as interchangeable, resilient, and swappable at runtime — the way
a gateway/proxy would.

It is demo/reference code for study and interview prep, not a production
service.

## Package management

- Use **uv** exclusively. Do not use `pip` directly, `poetry`, or `conda`.
- Dependencies are tracked in `requirements.txt` (not `pyproject.toml`).
  Install with:

  ```bash
  uv venv
  uv pip install -r requirements.txt
  ```

- When adding a new dependency, append it to `requirements.txt` and re-run
  `uv pip install -r requirements.txt`. Do not use `uv add`.

## Code layout

- `gateway/` — the thin wrapper around `init_chat_model` that all demos build on.
- `demos/demo_NN_*.py` — one self-contained script per LangChain gateway
  feature. Each has a `main()` entry point and a module docstring explaining
  *why* the feature matters, not just what the code does.
- `main.py` — CLI menu that runs any demo by number.

## Conventions

- Keep each demo runnable standalone (`python demos/demo_0X_....py` or via
  `main.py`), with no dependency on the others.
- Prefer LangChain's provider-agnostic APIs (`init_chat_model`, `Runnable`
  methods) over provider-specific SDK calls, since the point of the repo is
  the gateway abstraction.
- Do not commit `.env`, API keys, or `.venv/`.
- Keep comments limited to explaining *why* a feature matters, not restating
  the code.
