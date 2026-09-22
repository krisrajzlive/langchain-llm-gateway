"""Runtime-selectable models/params — the core "gateway" pattern.

Build one Runnable with `configurable_fields` / `configurable_alternatives`
and let each call pick the provider, model, or temperature at invoke time
via `.with_config(...)`, without rebuilding the chain.
"""

import os

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
        huggingface_llama=get_model(
            "meta-llama/Llama-3.1-8B-Instruct",
            model_provider="openai",
            base_url="https://router.huggingface.co/v1",
            api_key=os.environ["HUGGINGFACE_API_KEY"],
        ),
    )

    default_response = model.invoke("Say hello in five words or fewer.")
    print(f"[default: openai_mini] {default_response.content}")

    alt_response = model.with_config(
        configurable={"model": "huggingface_llama", "temperature": 0.9}
    ).invoke("Say hello in five words or fewer.")
    print(f"[configured: huggingface_llama, temp=0.9] {alt_response.content}")


if __name__ == "__main__":
    main()
