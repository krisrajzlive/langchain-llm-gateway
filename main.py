"""CLI menu to run any LangChain LLM Gateway demo.

Usage:
    python main.py            # interactive menu
    python main.py 3          # run demo 3 directly
"""

import importlib
import sys

DEMOS = {
    "1": ("Basic provider-agnostic gateway", "demos.demo_01_basic_gateway"),
    "2": ("Automatic provider fallback", "demos.demo_02_fallbacks"),
    "3": ("Retries + client-side rate limiting", "demos.demo_03_retry_and_rate_limit"),
    "4": ("Response caching", "demos.demo_04_caching"),
    "5": ("Token streaming", "demos.demo_05_streaming"),
    "6": ("Structured output", "demos.demo_06_structured_output"),
    "7": ("Tool calling", "demos.demo_07_tool_calling"),
    "8": ("Runtime-configurable model/params", "demos.demo_08_configurable_alternatives"),
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
