"""Spend limits: a budget cap enforced via a LangChain callback handler.

LangChain doesn't ship a dollar-denominated budget limiter out of the box
(only call-count limits, see demo 11), so this shows how a gateway operator
would build one: a `BaseCallbackHandler` that prices every response's token
usage and raises once cumulative spend crosses a cap. This is the same hook
point LangSmith/observability integrations use to meter usage.
"""

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult

from gateway import get_model

# Illustrative pricing, USD per 1K tokens (gpt-4o-mini rates, approximate).
PRICE_PER_1K_INPUT = 0.00015
PRICE_PER_1K_OUTPUT = 0.0006


class BudgetExceededError(Exception):
    pass


class SpendLimitCallback(BaseCallbackHandler):
    raise_error = True  # let BudgetExceededError propagate out of model.invoke()

    def __init__(self, budget_usd: float) -> None:
        self.budget_usd = budget_usd
        self.spent_usd = 0.0

    def on_llm_end(self, response: LLMResult, **kwargs) -> None:
        usage = (response.llm_output or {}).get("token_usage", {})
        input_tokens = usage.get("prompt_tokens", 0)
        output_tokens = usage.get("completion_tokens", 0)
        cost = (input_tokens / 1000) * PRICE_PER_1K_INPUT + (
            output_tokens / 1000
        ) * PRICE_PER_1K_OUTPUT
        self.spent_usd += cost
        print(f"  [spend tracker] +${cost:.6f} (total ${self.spent_usd:.6f} / ${self.budget_usd:.6f})")
        if self.spent_usd > self.budget_usd:
            raise BudgetExceededError(
                f"Budget of ${self.budget_usd:.6f} exceeded (spent ${self.spent_usd:.6f})"
            )


def main() -> None:
    budget = SpendLimitCallback(budget_usd=0.00001)  # deliberately tiny, to trip mid-run
    model = get_model("openai:gpt-4o-mini", callbacks=[budget])

    prompts = [
        "Say hello.",
        "Name a color.",
        "Count to three.",
    ]
    for prompt in prompts:
        try:
            response = model.invoke(prompt)
            print(f"[{prompt}] -> {response.content}")
        except BudgetExceededError as exc:
            print(f"Blocked: {exc}")
            break


if __name__ == "__main__":
    main()
