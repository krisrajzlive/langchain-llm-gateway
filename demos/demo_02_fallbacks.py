"""Automatic provider fallback with `with_fallbacks`.

If the primary model raises (bad model name, outage, rate limit, missing
key), the gateway transparently retries the same request against the next
model in the chain.
"""

import os

from gateway import get_model


def main() -> None:
    primary = get_model("openai:gpt-4o-mini-does-not-exist")
    backup = get_model(
        "meta-llama/Llama-3.1-8B-Instruct",
        model_provider="openai",
        base_url="https://router.huggingface.co/v1",
        api_key=os.environ["HUGGINGFACE_API_KEY"],
    )

    model_with_fallback = primary.with_fallbacks([backup])

    response = model_with_fallback.invoke("Name one benefit of a model gateway.")
    print(response.content)


if __name__ == "__main__":
    main()
