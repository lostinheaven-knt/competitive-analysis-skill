#!/usr/bin/env python3
import csv
import itertools
import sys
from typing import List


FIELDS = [
    "brand",
    "platform",
    "evidence_level",
    "source_type",
    "direct_observation_summary",
    "style_keywords",
    "age_signal",
    "price_signal",
    "content_signal",
    "category_or_hot_sku_signal",
    "channel_signal",
    "overlap_with_target",
    "target_overlap_score",
    "style_overlap_fit",
    "age_overlap_fit",
    "price_overlap_fit",
    "content_overlap_fit",
    "channel_overlap_fit",
    "competition_bucket",
    "competitor_type",
    "inclusion_reason",
    "main_gap",
    "source_reference",
]

DEFAULT_PLATFORMS = ["taobao", "douyin", "xiaohongshu", "brand-site"]


def parse_csvish(text: str) -> List[str]:
    return [item.strip() for item in text.split(",") if item.strip()]


def main() -> None:
    if len(sys.argv) not in (2, 3):
        print("Usage: platform_evidence_template.py <brand1,brand2,...> [platform1,platform2,...]", file=sys.stderr)
        sys.exit(1)

    brands = parse_csvish(sys.argv[1])
    if not brands:
        print("At least one brand is required", file=sys.stderr)
        sys.exit(1)

    platforms = parse_csvish(sys.argv[2]) if len(sys.argv) == 3 else DEFAULT_PLATFORMS
    if not platforms:
        print("At least one platform is required", file=sys.stderr)
        sys.exit(1)

    writer = csv.DictWriter(sys.stdout, fieldnames=FIELDS)
    writer.writeheader()
    for brand, platform in itertools.product(brands, platforms):
        writer.writerow({field: "" for field in FIELDS} | {"brand": brand, "platform": platform})


if __name__ == "__main__":
    main()
