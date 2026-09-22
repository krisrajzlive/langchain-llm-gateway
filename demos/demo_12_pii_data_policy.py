"""Data policy: PII detection/redaction via `PIIMiddleware`.

A gateway commonly enforces "don't let PII cross this boundary" as policy.
Here three strategies are shown against the same input containing an email
and a credit card number: `redact` (placeholder), `mask` (partial), and
`block` (raise and stop the call).
"""

from langchain.agents import create_agent
from langchain.agents.middleware import PIIDetectionError, PIIMiddleware
from langchain_core.messages import HumanMessage

from gateway import get_model

SENSITIVE_INPUT = (
    "My email is jane.doe@example.com and my card number is 4111 1111 1111 1111. "
    "Can you help me update my billing info?"
)


def run_with_strategy(strategy: str) -> None:
    agent = create_agent(
        get_model("openai:gpt-4o-mini"),
        middleware=[
            PIIMiddleware("email", strategy=strategy),
            PIIMiddleware("credit_card", strategy=strategy),
        ],
    )
    print(f"\n--- strategy={strategy} ---")
    try:
        result = agent.invoke({"messages": [HumanMessage(SENSITIVE_INPUT)]})
        redacted_user_message = result["messages"][0]
        print("What the model actually saw:", redacted_user_message.content)
        print("Model reply:", result["messages"][-1].content)
    except PIIDetectionError as exc:
        print("Blocked:", exc)


def main() -> None:
    for strategy in ["redact", "mask", "block"]:
        run_with_strategy(strategy)


if __name__ == "__main__":
    main()
