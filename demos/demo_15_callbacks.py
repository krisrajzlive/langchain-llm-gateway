"""LangChain's callback system: the hook points a gateway is built on.

Every gateway feature demonstrated elsewhere in this repo is secretly a
callback under the hood -- demo 10's spend limiter used `on_llm_end` to
price token usage, and observability tools like LangSmith attach a
callback handler to every run to capture traces. This demo makes those
hook points explicit by implementing one handler that logs the full
lifecycle of an agent run: model start/end, streamed tokens, and tool
start/end.

Callbacks fire regardless of *how* you invoke (`.invoke()`, `.stream()`,
inside an agent loop), which is what makes them the right layer for
cross-cutting concerns (metering, logging, guardrails, tracing) instead of
threading that logic through every call site by hand.
"""

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

from langchain.agents import create_agent

from gateway import get_model


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"It is sunny and 22C in {city}."


class LifecycleLoggingCallback(BaseCallbackHandler):
    """Logs every stage of a model/tool call as it happens."""

    def __init__(self) -> None:
        self.token_count = 0

    def on_chat_model_start(self, serialized, messages, **kwargs) -> None:
        print("  [callback] on_chat_model_start -> sending request to the model")

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        # Fires once per streamed token; counted rather than printed to
        # keep output readable for anything longer than a few tokens.
        self.token_count += 1

    def on_llm_end(self, response, **kwargs) -> None:
        usage = (response.llm_output or {}).get("token_usage", {})
        print(
            f"  [callback] on_llm_end -> model responded "
            f"(streamed_tokens_seen={self.token_count}, "
            f"completion_tokens={usage.get('completion_tokens')})"
        )

    def on_llm_error(self, error: BaseException, **kwargs) -> None:
        print(f"  [callback] on_llm_error -> {error!r}")

    def on_tool_start(self, serialized, input_str, **kwargs) -> None:
        print(f"  [callback] on_tool_start -> calling '{serialized.get('name')}' with {input_str!r}")

    def on_tool_end(self, output, **kwargs) -> None:
        print(f"  [callback] on_tool_end -> tool returned {output!r}")

    def on_chain_start(self, serialized, inputs, **kwargs) -> None:
        print("  [callback] on_chain_start -> agent run started")

    def on_chain_end(self, outputs, **kwargs) -> None:
        print("  [callback] on_chain_end -> agent run finished")


def main() -> None:
    logger = LifecycleLoggingCallback()

    print("=== Part 1: streaming a single model call ===")
    model = get_model("openai:gpt-4o-mini")
    for _ in model.stream("Count from 1 to 5.", config={"callbacks": [logger]}):
        pass  # tokens are counted by the callback, not printed here

    print()
    print("=== Part 2: an agent run with a tool call ===")
    print(
        "(nested on_chain_start/end pairs below are real: create_agent builds"
        " a LangGraph state machine with its own nested chain boundaries)"
    )
    logger.token_count = 0
    agent = create_agent(get_model("openai:gpt-4o-mini"), tools=[get_weather])
    agent.invoke(
        {"messages": [HumanMessage("What's the weather in Chennai?")]},
        config={"callbacks": [logger]},
    )


if __name__ == "__main__":
    main()
