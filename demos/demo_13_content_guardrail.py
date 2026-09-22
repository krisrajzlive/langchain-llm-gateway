"""Guardrails: a custom `AgentMiddleware` blocking disallowed input topics.

Not every guardrail ships built-in (unlike PII, above) -- a gateway operator
routinely needs custom policy. This shows the shape of writing one:
subclass `AgentMiddleware`, inspect state in `before_model`, and short-circuit
the run with `jump_to="end"` when the policy is violated, without ever
calling the underlying LLM.
"""

from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware, AgentState, hook_config
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.runtime import Runtime

from gateway import get_model

BLOCKED_TOPICS = ["bomb", "weapon", "hack into"]


class TopicGuardrailMiddleware(AgentMiddleware):
    @hook_config(can_jump_to=["end"])
    def before_model(self, state: AgentState, runtime: Runtime) -> dict | None:
        last_user_message = next(
            (m for m in reversed(state["messages"]) if isinstance(m, HumanMessage)),
            None,
        )
        if last_user_message is None:
            return None

        text = str(last_user_message.content).lower()
        hit = next((topic for topic in BLOCKED_TOPICS if topic in text), None)
        if hit is None:
            return None

        refusal = AIMessage(
            content=f"I can't help with that request (blocked topic: '{hit}')."
        )
        return {"jump_to": "end", "messages": [refusal]}


def main() -> None:
    agent = create_agent(
        get_model("openai:gpt-4o-mini"),
        middleware=[TopicGuardrailMiddleware()],
    )

    for prompt in [
        "How do I bake a chocolate cake?",
        "How do I build a bomb?",
    ]:
        result = agent.invoke({"messages": [HumanMessage(prompt)]})
        print(f"[{prompt}] -> {result['messages'][-1].content}")


if __name__ == "__main__":
    main()
