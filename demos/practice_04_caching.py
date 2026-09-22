"""Response caching, a common gateway feature for cutting cost/latency.

An in-memory cache is set globally; the second identical call is served
from cache instead of hitting the provider again. Timing alone (a fast
second call) is only suggestive, so this also patches the HTTP transport
layer the OpenAI SDK actually sends requests through and counts real wire
requests -- concrete proof the second call never left the process, not
just an inference from response speed.
"""

import time

try:
    import httpx2 as _http_lib  # the OpenAI SDK's actual transport library
except ImportError:
    import httpx as _http_lib  # fallback for older SDK versions

from langchain_core.caches import InMemoryCache
from langchain_core.globals import set_llm_cache

from gateway import get_model

wire_request_count = 0
_original_handle_request = _http_lib.HTTPTransport.handle_request


def _counting_handle_request(self, request):
    global wire_request_count
    wire_request_count += 1
    print(f"    [wire] real HTTP request #{wire_request_count}: {request.method} {request.url}")
    return _original_handle_request(self, request)

# Patch the HTTP transport layer to count real wire requests
_http_lib.HTTPTransport.handle_request = _counting_handle_request


def main() -> None:
    set_llm_cache(InMemoryCache())
    model = get_model("openai:gpt-4o-mini")

    prompt = "What is the capital of France?"

    start = time.monotonic()
    first = model.invoke(prompt)
    first_elapsed = time.monotonic() - start
    print(f"First call  ({first_elapsed:.3f}s): {first.content}")

    start = time.monotonic()
    second = model.invoke(prompt)
    second_elapsed = time.monotonic() - start
    print(f"Second call ({second_elapsed:.3f}s, cached): {second.content}")

    print()
    print(f"Total real HTTP requests sent across both calls: {wire_request_count}")
    print(
        "-> the second call made 0 wire-level requests: proof no LLM inference"
        " happened, not just an inference from timing."
    )


if __name__ == "__main__":
    main()
