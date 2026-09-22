"""Automatic provider fallback with `with_fallbacks`.

If the primary model raises (bad model name, outage, rate limit, missing
key), the gateway transparently retries the same request against the next
model in the chain. This chains three tiers -- OpenAI, Hugging Face, Ollama
Cloud -- with the first two deliberately misconfigured so the call visibly
cascades all the way down to the third, real provider.
"""

import os

from gateway import get_model


def main() -> None:
    primary = get_model("openai:gpt-4o-mini-does-not-exist")
    backup_1 = get_model(
        "does-not-exist",
        model_provider="openai",
        base_url="https://router.huggingface.co/v1",
        api_key=os.environ["HUGGINGFACE_API_KEY"],
    )
    backup_2 = get_model(
        "gpt-oss:20b",
        model_provider="openai",
        base_url="https://ollama.com/v1",
        api_key=os.environ["OLLAMA_API_KEY"],
    )

    model_with_fallback = primary.with_fallbacks([backup_1, backup_2])

    response = model_with_fallback.invoke("Name one benefit of a model gateway.")
    print(response.content)


if __name__ == "__main__":
    main()
