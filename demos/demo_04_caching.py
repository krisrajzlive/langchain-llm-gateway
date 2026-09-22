"""Response caching, a common gateway feature for cutting cost/latency.

An in-memory cache is set globally; the second identical call is served
from cache instead of hitting the provider again.
"""

import time

from langchain_core.caches import InMemoryCache
from langchain_core.globals import set_llm_cache

from gateway import get_model


def main() -> None:
    set_llm_cache(InMemoryCache())
    model = get_model("openai:gpt-4o-mini")

    prompt = "What is the capital of France?"

    start = time.monotonic()
    first = model.invoke(prompt)
    first_elapsed = time.monotonic() - start

    start = time.monotonic()
    second = model.invoke(prompt)
    second_elapsed = time.monotonic() - start

    print(f"First call  ({first_elapsed:.3f}s): {first.content}")
    print(f"Second call ({second_elapsed:.3f}s, cached): {second.content}")


if __name__ == "__main__":
    main()
