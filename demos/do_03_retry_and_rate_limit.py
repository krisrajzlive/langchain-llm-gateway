"""Resilience knobs a gateway typically owns: retries and client-side rate limiting.

`with_retry` retries transient failures with backoff. `InMemoryRateLimiter`
throttles outbound requests so a burst of calls doesn't trip provider limits.
"""

import time

from langchain_core.rate_limiters import InMemoryRateLimiter

from gateway import get_model


def main() -> None:
    rate_limiter = InMemoryRateLimiter(
        requests_per_second=0.5,  # one request every 2 seconds
        check_every_n_seconds=0.1,
        max_bucket_size=1,
    )

    model = get_model("openai:gpt-4o-mini", rate_limiter=rate_limiter).with_retry(
        stop_after_attempt=3,
        wait_exponential_jitter=True,
    )

    start = time.monotonic()
    for prompt in ["Say 'one'.", "Say 'two'."]:
        response = model.invoke(prompt)
        elapsed = time.monotonic() - start
        print(f"[t={elapsed:5.1f}s] {response.content}")


if __name__ == "__main__":
    main()
