"""Hugging Face Inference Providers: a free, OpenAI-compatible LLM gateway.

`router.huggingface.co/v1` is an OpenAI-compatible chat-completions endpoint
that routes to multiple backend inference providers behind one API and one
token. Since it's OpenAI-compatible, it plugs into LangChain's gateway the
same way as any other provider: `init_chat_model` with `model_provider`
forced to "openai" and a custom `base_url`.
"""

import os

from gateway import get_model


def main() -> None:
    model = get_model(
        "meta-llama/Llama-3.1-8B-Instruct",
        model_provider="openai",
        base_url="https://router.huggingface.co/v1",
        api_key=os.environ["HUGGINGFACE_API_KEY"],
    )
    response = model.invoke("In one short sentence, what is an LLM gateway?")
    print(response.content)


if __name__ == "__main__":
    main()
