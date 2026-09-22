"""Runtime-selectable models/params — the core "gateway" pattern.

Build one Runnable with `configurable_fields` / `configurable_alternatives`
and let each call pick the provider, model, or temperature at invoke time
via `.with_config(...)`, without rebuilding the chain.
"""

from langchain_core.runnables import ConfigurableField

from gateway import get_model


def main() -> None:
    model = get_model("openai:gpt-4o-mini", temperature=0).configurable_fields(
        temperature=ConfigurableField(
            id="temperature",
            name="LLM Temperature",
            description="The temperature of the LLM",
        )
    ).configurable_alternatives(
        ConfigurableField(id="model"),
        default_key="openai_mini",
        anthropic_haiku=get_model("anthropic:claude-3-5-haiku-latest"),
    )

    default_response = model.invoke("Say hello in five words or fewer.")
    print(f"[default: openai_mini] {default_response.content}")

    alt_response = model.with_config(
        configurable={"model": "anthropic_haiku", "temperature": 0.9}
    ).invoke("Say hello in five words or fewer.")
    print(f"[configured: anthropic_haiku, temp=0.9] {alt_response.content}")


if __name__ == "__main__":
    main()
