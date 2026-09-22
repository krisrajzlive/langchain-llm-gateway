"""Tool calling through the gateway with `bind_tools`.

The model decides when to call a tool; the caller is responsible for
executing it and, if desired, feeding the result back for a final answer.
"""

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

from gateway import get_model


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"It is sunny and 22C in {city}."


def main() -> None:
    model = get_model("openai:gpt-4o-mini").bind_tools([get_weather])

    messages = [HumanMessage("What's the weather like in Chennai?")]
    ai_message = model.invoke(messages)
    messages.append(ai_message)

    for call in ai_message.tool_calls:
        result = get_weather.invoke(call["args"])
        messages.append(
            {"role": "tool", "content": result, "tool_call_id": call["id"]}
        )

    final = model.invoke(messages)
    print(final.content)


if __name__ == "__main__":
    main()
