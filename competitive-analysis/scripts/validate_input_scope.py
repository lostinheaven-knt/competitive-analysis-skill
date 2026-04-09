#!/usr/bin/env python3
import json
import sys

REQUIRED = ["target", "industry", "region", "target_customer", "goal"]

PROMPTS = {
    "target": "What exactly are we analyzing: company, brand, product, or solution?",
    "industry": "Which industry or category does the target belong to?",
    "region": "Which market matters most: local, national, regional, or global?",
    "target_customer": "Who is the target customer?",
    "goal": "What do you need: framework, candidate list, shortlist, benchmark, or full report?",
    "channel": "Which sales or distribution channel matters most?",
    "price_band": "Which price band or commercial tier should count as comparable?"
}


def main():
    data = json.load(sys.stdin)
    missing = [k for k in REQUIRED if not data.get(k)]
    optional_missing = [k for k in ["channel", "price_band"] if not data.get(k)]

    status = "ok" if not missing else "needs_clarification"
    questions = [PROMPTS[k] for k in missing + optional_missing[: max(0, 3 - len(missing))]]

    result = {
        "status": status,
        "missing_fields": missing,
        "recommended_questions": questions,
    }
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
