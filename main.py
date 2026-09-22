"""CLI menu to run any LangChain LLM Gateway demo.

Usage:
    python main.py            # interactive menu
    python main.py 3          # run demo 3 directly
"""

import importlib
import sys

DEMOS = {
    "1": ("Basic provider-agnostic gateway", "demos.do_01_basic_gateway"),
    "2": ("Automatic provider fallback", "demos.do_02_fallbacks"),
    "3": ("Retries + client-side rate limiting", "demos.do_03_retry_and_rate_limit"),
    "4": ("Response caching", "demos.do_04_caching"),
    "5": ("Token streaming", "demos.do_05_streaming"),
    "6": ("Structured output", "demos.do_06_structured_output"),
    "7": ("Tool calling", "demos.do_07_tool_calling"),
    "8": ("Runtime-configurable model/params", "demos.do_08_configurable_alternatives"),
    "9": ("Hugging Face Inference Providers (free gateway)", "demos.do_09_huggingface_gateway"),
    "10": ("Spend limit (budget cap via callback)", "demos.do_10_spend_limit"),
    "11": ("Call-count rate limit (ModelCallLimitMiddleware)", "demos.do_11_call_rate_limits"),
    "12": ("Data policy: PII redaction/masking/blocking", "demos.do_12_pii_data_policy"),
    "13": ("Guardrail: custom blocked-topic middleware", "demos.do_13_content_guardrail"),
    "14": ("Per-request reasoning effort (low/medium/high)", "demos.do_14_reasoning_effort"),
    "15": ("LLM callback lifecycle (model/tool/chain hooks)", "demos.do_15_callbacks"),
}


def run(choice: str) -> None:
    if choice not in DEMOS:
        print(f"Unknown demo '{choice}'. Choose from: {', '.join(DEMOS)}")
        sys.exit(1)
    label, module_name = DEMOS[choice]
    print(f"\n=== Demo {choice}: {label} ===\n")
    module = importlib.import_module(module_name)
    module.main()


def menu() -> None:
    print("LangChain LLM Gateway demos:")
    for key, (label, _) in DEMOS.items():
        print(f"  {key}. {label}")
    choice = input("Pick a demo number: ").strip()
    run(choice)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run(sys.argv[1])
    else:
        menu()
