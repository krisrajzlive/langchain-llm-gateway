"""Token streaming through the gateway, identical across providers."""

from gateway import get_model


def main() -> None:
    model = get_model("openai:gpt-4o-mini")

    for chunk in model.stream("Count from 1 to 5, one number per line."):
        print(chunk.content, end="", flush=True)
    print()


if __name__ == "__main__":
    main()
