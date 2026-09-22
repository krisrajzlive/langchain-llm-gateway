"""Per-request effort tuning: `reasoning_effort`, model and effort chosen interactively.

Unlike demos 1/2/8/9 (routing across *different* models/providers on
failure or by choice), this tunes an *individual* model's reasoning depth
per request -- the same lever Claude Code's desktop app exposes as a model
"effort" picker. Two independently-verified backends support the same
`reasoning_effort` parameter:

- OpenAI's GPT-5 family (native reasoning models; reports a precise
  `reasoning_tokens` count separate from the visible answer).
- `gpt-oss` (OpenAI's open-weight model family, served here via Ollama
  Cloud), trained with adjustable reasoning effort as a first-class
  feature.

Effort isn't just a label: token usage generally scales with it because
the model spends more of its budget reasoning before answering. OpenAI
reports an explicit `reasoning_tokens` count that rises cleanly and
monotonically with effort; `gpt-oss` via Ollama only exposes aggregate
`completion_tokens`, which trends upward but can vary run to run due to
sampling. Either way, this is direct, measurable evidence the parameter
changes real model behavior, not just longer-looking text.
"""

import os

from gateway import get_model

DEFAULT_PROMPT = "A farmer has 17 sheep. All but 9 die. How many are left? Explain briefly."

MODELS = {
    "1": ("openai:gpt-5-mini", {}),
    "2": (
        "gpt-oss:20b",
        {
            "model_provider": "openai",
            "base_url": "https://ollama.com/v1",
            "api_key": os.environ.get("OLLAMA_API_KEY"),
        },
    ),
}

EFFORTS = {"1": "low", "2": "medium", "3": "high"}


def _choose(prompt: str, options: dict[str, str]) -> str:
    print(prompt)
    for key, label in options.items():
        print(f"  {key}. {label}")
    choice = input("> ").strip()
    if choice not in options:
        print(f"Unrecognized choice '{choice}', defaulting to '1'.")
        choice = "1"
    return choice


def main() -> None:
    model_choice = _choose(
        "Pick a model:", {k: v[0] for k, v in MODELS.items()}
    )
    model_id, kwargs = MODELS[model_choice]

    effort_choice = _choose("Pick a reasoning effort:", EFFORTS)
    effort = EFFORTS[effort_choice]

    custom_prompt = input(f"Prompt [default: {DEFAULT_PROMPT!r}]: ").strip()
    user_prompt = custom_prompt or DEFAULT_PROMPT

    model = get_model(model_id, **kwargs)
    response = model.invoke(user_prompt, reasoning_effort=effort)

    usage = response.response_metadata.get("token_usage", {})
    reasoning_tokens = (usage.get("completion_tokens_details") or {}).get(
        "reasoning_tokens"
    )
    completion_tokens = usage.get("completion_tokens")

    detail = f"completion_tokens={completion_tokens}"
    if reasoning_tokens is not None:
        detail += f", reasoning_tokens={reasoning_tokens}"

    print()
    print(f"=== {model_id}, effort={effort} ===")
    print(f"  {detail}")
    print(f"  answer: {response.content}")


if __name__ == "__main__":
    main()
