#!/usr/bin/env python3
import csv
import sys

B2C_FIELDS = [
    "company_name",
    "brand_name",
    "product_name",
    "segment",
    "region",
    "target_customer",
    "channel",
    "price_band",
    "why_candidate",
    "evidence_type",
    "source_url_or_note",
    "confidence",
    "status",
]

B2B_FIELDS = [
    "company_name",
    "product_name",
    "category",
    "region",
    "target_customer",
    "deployment_model",
    "pricing_model",
    "channel",
    "why_candidate",
    "evidence_type",
    "source_url_or_note",
    "confidence",
    "status",
]


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "b2c"
    fields = B2B_FIELDS if mode.lower() == "b2b" else B2C_FIELDS

    writer = csv.DictWriter(sys.stdout, fieldnames=fields)
    writer.writeheader()
    writer.writerow({k: "" for k in fields})


if __name__ == "__main__":
    main()
