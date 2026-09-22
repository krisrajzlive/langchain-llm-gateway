"""Provider-agnostic model init via the gateway.

Swap providers/models by changing a string (or a base_url + provider pair
for an OpenAI-compatible endpoint), no code changes downstream.
"""

import os

from gateway import get_model

PROVIDERS = [
    ("openai:gpt-4o-mini", {}),
    (
        "meta-llama/Llama-3.1-8B-Instruct",
        {
            "model_provider": "openai",
            "base_url": "https://router.huggingface.co/v1",
            "api_key": os.environ.get("HUGGINGFACE_API_KEY"),
        },
    ),
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
    for model_id, kwargs in PROVIDERS:
        model = get_model(model_id, **kwargs)
        response = model.invoke("In one short sentence, what is LangChain?")
        print(f"[{model_id}] {response.content}")


if __name__ == "__main__":
    main()
