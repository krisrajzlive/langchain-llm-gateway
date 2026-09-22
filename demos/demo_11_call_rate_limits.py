"""Rate/call limits at the agent level via `ModelCallLimitMiddleware`.

Distinct from demo 3's client-side `InMemoryRateLimiter` (which throttles
request timing): this caps *how many* model calls an agent run/thread may
make at all, and ends the run cleanly once the cap is hit -- the agent-loop
equivalent of a gateway's per-key request quota.
"""

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

from gateway import get_model


@tool
def get_time() -> str:
    """Return a fixed, fake current time (demo tool)."""
    return "14:32 UTC"


def main() -> None:
    call_limiter = ModelCallLimitMiddleware(run_limit=1, exit_behavior="end")

    agent = create_agent(
        get_model("openai:gpt-4o-mini"),
        tools=[get_time],
        middleware=[call_limiter],
    )

    result = agent.invoke(
        {
            "messages": [
                HumanMessage(
                    "What time is it, and then tell me the weather forecast "
                    "for that time too."
                )
            ]
        }
    )
    for message in result["messages"]:
        print(f"[{message.type}] {message.content}")


if __name__ == "__main__":
    main()
