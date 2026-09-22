"""Per-request effort tuning across multiple models: `reasoning_effort`.

Unlike demos 1/2/8/9 (routing across *different* models/providers on
failure or by choice), this tunes each *individual* model's reasoning
depth per request -- the same lever Claude Code's desktop app exposes as
a model "effort" picker. Two independently-verified backends support the
same `reasoning_effort` parameter:

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

PROMPT = "A farmer has 17 sheep. All but 9 die. How many are left? Explain briefly."

MODELS = [
    ("openai:gpt-5-mini", {}),
    (
        "gpt-oss:20b",
        {
            "model_provider": "openai",
            "base_url": "https://ollama.com/v1",
            "api_key": os.environ.get("OLLAMA_API_KEY"),
        },
    ),
]


def main() -> None:
    for model_id, kwargs in MODELS:
        model = get_model(model_id, **kwargs)
        print(f"=== {model_id} ===")
        for effort in ["low", "medium", "high"]:
            response = model.invoke(PROMPT, reasoning_effort=effort)
            usage = response.response_metadata.get("token_usage", {})
            reasoning_tokens = (usage.get("completion_tokens_details") or {}).get(
                "reasoning_tokens"
            )
            completion_tokens = usage.get("completion_tokens")

            detail = f"completion_tokens={completion_tokens}"
            if reasoning_tokens is not None:
                detail += f", reasoning_tokens={reasoning_tokens}"

            print(f"  effort={effort:6s} {detail}")
            print(f"    -> {response.content.splitlines()[0][:100]}")
        print()


if __name__ == "__main__":
    main()
