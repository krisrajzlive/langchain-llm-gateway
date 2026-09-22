"""Automatic provider fallback with `with_fallbacks`.

If the primary model raises (bad model name, outage, rate limit, missing
key), the gateway transparently retries the same request against the next
model in the chain.
"""

from gateway import get_model


def main() -> None:
    primary = get_model("openai:gpt-4o-mini-does-not-exist")
    backup = get_model("anthropic:claude-3-5-haiku-latest")

    model_with_fallback = primary.with_fallbacks([backup])

    response = model_with_fallback.invoke("Name one benefit of a model gateway.")
    print(response.content)


if __name__ == "__main__":
    main()
