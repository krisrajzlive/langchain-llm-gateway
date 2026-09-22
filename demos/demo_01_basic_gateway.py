"""Provider-agnostic model init via the gateway.

Swap providers/models by changing a string, no code changes downstream.
"""

from gateway import get_model


def main() -> None:
    for model_id in ["openai:gpt-4o-mini", "anthropic:claude-3-5-haiku-latest"]:
        model = get_model(model_id)
        response = model.invoke("In one short sentence, what is LangChain?")
        print(f"[{model_id}] {response.content}")


if __name__ == "__main__":
    main()
