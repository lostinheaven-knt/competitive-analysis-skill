#!/usr/bin/env python3
"""Convert row-level platform evidence into candidate-level scoring inputs.

Heuristic boundary:
- This script is a deterministic bridge from platform evidence rows to candidate-level fields.
- The numeric mappings and bucket rules in this file are lightweight heuristics for shortlist support,
  not authoritative market truth or investment-grade scoring logic.
- Prefer explicit analyst-entered fit values from the evidence table when available.
- Treat the derived scores as structured inputs for ranking and reporting, then verify the final
  shortlist against raw evidence before treating the output as definitive.
"""

import csv
import json
import math
import re
import sys
from collections import Counter, defaultdict
from typing import Any, Dict, List, Optional, Set, Tuple


FIT_LABELS = {
    "very-high": 0.95,
    "very high": 0.95,
    "high": 0.85,
    "medium-high": 0.75,
    "medium high": 0.75,
    "medium": 0.6,
    "medium-low": 0.45,
    "medium low": 0.45,
    "low": 0.3,
    "very-low": 0.15,
    "very low": 0.15,
    "direct": 0.9,
    "secondary": 0.6,
    "watchlist": 0.3,
    "strong": 0.8,
    "weak": 0.35,
}

EVIDENCE_LEVELS = {
    "high": 0.9,
    "medium_high": 0.78,
    "medium-high": 0.78,
    "medium high": 0.78,
    "medium": 0.62,
    "low_medium": 0.48,
    "low-medium": 0.48,
    "low medium": 0.48,
    "low": 0.32,
}

SPLIT_RE = re.compile(r"[|,;、/\\\n]+")
NUMBER_RE = re.compile(r"\d+(?:\.\d+)?")


def load_rows(path: str) -> List[Dict[str, Any]]:
    lower = path.lower()
    if lower.endswith(".csv"):
        with open(path, "r", encoding="utf-8") as f:
            return [dict(row) for row in csv.DictReader(f)]
    if lower.endswith(".json"):
        with open(path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        if isinstance(payload, list):
            return [row for row in payload if isinstance(row, dict)]
        if isinstance(payload, dict) and isinstance(payload.get("observations"), list):
            return [row for row in payload["observations"] if isinstance(row, dict)]
    raise ValueError("platform evidence input must be csv or json")


def stringify(value: Any, default: str = "") -> str:
    if value is None:
        return default
    if isinstance(value, str):
        text = value.strip()
        return text if text else default
    return str(value)


def split_points(value: Any) -> List[str]:
    text = stringify(value)
    if not text:
        return []
    return [item.strip(" -•\t") for item in SPLIT_RE.split(text) if item.strip(" -•\t")]


def dedupe_keep_order(items: List[str]) -> List[str]:
    seen = set()
    out: List[str] = []
    for item in items:
        key = item.strip().casefold()
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def mean(values: List[float]) -> Optional[float]:
    if not values:
        return None
    return sum(values) / len(values)


def jaccard(a: Set[str], b: Set[str]) -> Optional[float]:
    if not a or not b:
        return None
    union = a | b
    if not union:
        return None
    return len(a & b) / len(union)


def parse_scaled_number(text: str) -> Optional[float]:
    text = stringify(text).casefold()
    if not text:
        return None
    try:
        value = float(text)
        if value > 1:
            return clamp(value / 100 if value <= 100 else 1.0)
        return clamp(value)
    except ValueError:
        return None


def parse_fit(value: Any) -> Optional[float]:
    text = stringify(value).casefold()
    if not text:
        return None
    numeric = parse_scaled_number(text)
    if numeric is not None:
        return numeric
    for label, score in FIT_LABELS.items():
        if label in text:
            return score
    if "最贴脸" in text or "高度重合" in text or "高重合" in text:
        return 0.9
    if "强相关" in text or "较高重合" in text:
        return 0.72
    if "市场压力" in text or "watchlist" in text:
        return 0.35
    if "弱" in text or "不高" in text:
        return 0.35
    return None


def parse_evidence_level(value: Any) -> Optional[float]:
    text = stringify(value).casefold().replace(" ", "_")
    if not text:
        return None
    numeric = parse_scaled_number(text)
    if numeric is not None:
        return numeric
    for label, score in EVIDENCE_LEVELS.items():
        if label in text:
            return score
    return None


def infer_competitor_type(row: Dict[str, Any]) -> str:
    raw = stringify(row.get("competitor_type") or row.get("competition_bucket") or row.get("overlap_with_target")).casefold()
    if any(token in raw for token in ["direct", "最贴脸", "核心竞品"]):
        return "direct"
    if any(token in raw for token in ["secondary", "强相关", "防守"]):
        return "secondary"
    if any(token in raw for token in ["watchlist", "观察", "压力", "market pressure"]):
        return "watchlist"
    return "secondary"


def tokenize_keywords(value: Any) -> Set[str]:
    return {item.casefold() for item in split_points(value)}


def age_buckets(text: Any) -> Set[str]:
    raw = stringify(text).casefold()
    buckets: Set[str] = set()
    if not raw:
        return buckets
    if any(token in raw for token in ["0-18", "0-12", "0-14"]):
        buckets.add("broad-child")
    if any(token in raw for token in ["0-3", "婴", "baby", "infant"]):
        buckets.add("infant")
    if any(token in raw for token in ["3-6", "幼儿", "preschool"]):
        buckets.add("preschool")
    if any(token in raw for token in ["3-12", "school-age", "儿童"]):
        buckets.add("school-age")
    if any(token in raw for token in ["中大童", "中学生", "初中生", "高中生", "teen", "少女"]):
        buckets.add("older-girl-school")
    if "女童" in raw or "girls" in raw:
        buckets.add("girls")
    if not buckets:
        buckets.add("generic")
    return buckets


def price_buckets(text: Any) -> Set[str]:
    raw = stringify(text).casefold()
    buckets: Set[str] = set()
    numbers = [float(n) for n in NUMBER_RE.findall(raw)]
    if any(token in raw for token in ["大众", "低价", "平价", "mass"]):
        buckets.add("low")
    if any(token in raw for token in ["中端", "mid"]):
        buckets.add("mid")
    if any(token in raw for token in ["中高端", "upper-mid", "premium"]):
        buckets.add("upper-mid")
    if any(token in raw for token in ["高端", "luxury"]):
        buckets.add("high")
    if numbers:
        if any(n <= 120 for n in numbers):
            buckets.add("low")
        if any(80 <= n <= 260 for n in numbers):
            buckets.add("mid")
        if any(180 <= n <= 520 for n in numbers):
            buckets.add("upper-mid")
        if any(n >= 500 for n in numbers):
            buckets.add("high")
    return buckets


def content_tokens(text: Any) -> Set[str]:
    return tokenize_keywords(text)


def channel_tokens(platforms: Set[str], text: Any) -> Set[str]:
    tokens = set(platforms)
    raw = stringify(text).casefold()
    for token in ["ecommerce", "电商", "content", "内容", "社群", "private domain", "线下", "retail", "旗舰店"]:
        if token in raw:
            tokens.add(token)
    return tokens


def pick_text(row: Dict[str, Any], *keys: str) -> str:
    for key in keys:
        text = stringify(row.get(key))
        if text:
            return text
    return ""


def aggregate_rows(rows: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    grouped: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
        "rows": [],
        "platforms": set(),
        "evidence_scores": [],
        "style_tokens": set(),
        "age_buckets": set(),
        "price_buckets": set(),
        "content_tokens": set(),
        "channel_tokens": set(),
        "main_gaps": [],
        "evidence_points": [],
        "source_refs": 0,
        "direct_obs_rows": 0,
        "fit_values": defaultdict(list),
        "competitor_types": [],
        "competition_buckets": [],
        "inclusion_reasons": [],
    })

    for row in rows:
        brand = stringify(row.get("brand") or row.get("candidate") or row.get("name"))
        if not brand:
            continue
        g = grouped[brand]
        g["rows"].append(row)
        platform = stringify(row.get("platform"), default="mixed").casefold()
        if platform:
            g["platforms"].add(platform)
        evidence_score = parse_evidence_level(row.get("evidence_level"))
        if evidence_score is not None:
            g["evidence_scores"].append(evidence_score)
        style = pick_text(row, "style_keywords")
        g["style_tokens"].update(tokenize_keywords(style))
        g["age_buckets"].update(age_buckets(pick_text(row, "age_signal")))
        g["price_buckets"].update(price_buckets(pick_text(row, "price_signal")))
        g["content_tokens"].update(content_tokens(pick_text(row, "content_signal")))
        g["channel_tokens"].update(channel_tokens({platform} if platform else set(), pick_text(row, "channel_signal")))
        gap = pick_text(row, "main_gap")
        if gap:
            g["main_gaps"].append(gap)
        evidence_bits = [
            pick_text(row, "direct_observation_summary"),
            pick_text(row, "platform_evidence"),
            pick_text(row, "brand_page_evidence"),
        ]
        for bit in evidence_bits:
            if bit:
                g["evidence_points"].append(bit)
        if pick_text(row, "direct_observation_summary", "platform_evidence"):
            g["direct_obs_rows"] += 1
        if pick_text(row, "source_reference"):
            g["source_refs"] += 1
        g["competitor_types"].append(infer_competitor_type(row))
        bucket = pick_text(row, "competition_bucket")
        if bucket:
            g["competition_buckets"].append(bucket)
        reason = pick_text(row, "inclusion_reason")
        if reason:
            g["inclusion_reasons"].append(reason)

        for field, key in [
            ("target_overlap", "overlap_with_target"),
            ("target_overlap", "target_overlap_score"),
            ("style", "style_overlap_fit"),
            ("age", "age_overlap_fit"),
            ("price", "price_overlap_fit"),
            ("content", "content_overlap_fit"),
            ("channel", "channel_overlap_fit"),
        ]:
            score = parse_fit(row.get(key))
            if score is not None:
                g["fit_values"][field].append(score)
    return grouped


def score_from_similarity(explicit: List[float], generic: List[float], similarity: Optional[float], fallback: Optional[float] = None) -> Optional[float]:
    if explicit:
        return mean(explicit)
    if generic:
        return mean(generic)
    if similarity is not None:
        return similarity
    return fallback


def summary_line(label: str, values: List[str], limit: int = 3) -> Optional[str]:
    cleaned = [v for v in dedupe_keep_order(values) if v]
    if not cleaned:
        return None
    return f"{label}: {'; '.join(cleaned[:limit])}"


def build_candidate_output(grouped: Dict[str, Dict[str, Any]], target_brand: str) -> List[Dict[str, Any]]:
    target = grouped.get(target_brand)
    target_style = target["style_tokens"] if target else set()
    target_age = target["age_buckets"] if target else set()
    target_price = target["price_buckets"] if target else set()
    target_content = target["content_tokens"] if target else set()
    target_channel = target["channel_tokens"] if target else set()

    outputs: List[Dict[str, Any]] = []
    for brand, data in grouped.items():
        if brand == target_brand:
            continue

        row_count = len(data["rows"]) or 1
        platform_count = len(data["platforms"]) if data["platforms"] else 1
        avg_evidence = mean(data["evidence_scores"]) or 0.5
        direct_obs_ratio = data["direct_obs_rows"] / row_count
        source_ref_ratio = min(data["source_refs"] / row_count, 1.0)
        platform_coverage = min(platform_count / 4, 1.0)
        gap_penalty = 0.08 if len(data["main_gaps"]) >= row_count else 0.0

        generic_overlap = data["fit_values"]["target_overlap"]
        style_score = score_from_similarity(data["fit_values"]["style"], generic_overlap, jaccard(data["style_tokens"], target_style), fallback=0.5 if target_style else None)
        age_score = score_from_similarity(data["fit_values"]["age"], generic_overlap, jaccard(data["age_buckets"], target_age), fallback=0.5 if target_age else None)
        price_score = score_from_similarity(data["fit_values"]["price"], generic_overlap, jaccard(data["price_buckets"], target_price), fallback=0.5 if target_price else None)
        content_score = score_from_similarity(data["fit_values"]["content"], generic_overlap, jaccard(data["content_tokens"], target_content), fallback=0.5 if target_content else None)
        channel_score = score_from_similarity(data["fit_values"]["channel"], generic_overlap, jaccard(data["channel_tokens"], target_channel), fallback=platform_coverage)

        platform_evidence_score = clamp((avg_evidence + direct_obs_ratio + platform_coverage) / 3)
        evidence_confidence_score = clamp(avg_evidence * 0.55 + direct_obs_ratio * 0.2 + source_ref_ratio * 0.15 + platform_coverage * 0.1 - gap_penalty)

        competitor_type = Counter(data["competitor_types"]).most_common(1)[0][0] if data["competitor_types"] else "secondary"
        competition_bucket = data["competition_buckets"][0] if data["competition_buckets"] else competitor_type
        inclusion_reason = data["inclusion_reasons"][0] if data["inclusion_reasons"] else "Platform evidence suggests meaningful overlap with the target brand."

        evidence_points: List[str] = []
        overlap_keywords = sorted(data["style_tokens"] & target_style)[:4] if target_style else sorted(list(data["style_tokens"]))[:4]
        if overlap_keywords:
            evidence_points.append(f"Style overlap keywords: {', '.join(overlap_keywords)}")
        line = summary_line("Observed evidence", data["evidence_points"], limit=2)
        if line:
            evidence_points.append(line)
        if data["platforms"]:
            evidence_points.append(f"Observed platforms: {', '.join(sorted(data['platforms']))}")

        uncertainty_points = dedupe_keep_order(data["main_gaps"])
        if not uncertainty_points:
            uncertainty_points.append("Platform evidence is only as strong as the currently observable public pages.")

        ranking_logic = (
            "Platform-informed score combining style overlap, age fit, price fit, content overlap, "
            "channel fit, and evidence confidence."
        )

        outputs.append(
            {
                "candidate": brand,
                "name": brand,
                "competitor_type": competitor_type,
                "competition_bucket": competition_bucket,
                "inclusion_reason": inclusion_reason,
                "major_evidence_points": evidence_points,
                "major_uncertainty_points": uncertainty_points,
                "ranking_logic": ranking_logic,
                "style_overlap_score": round(style_score, 4) if style_score is not None else None,
                "age_overlap_score": round(age_score, 4) if age_score is not None else None,
                "price_fit_score": round(price_score, 4) if price_score is not None else None,
                "content_overlap_score": round(content_score, 4) if content_score is not None else None,
                "channel_fit_score": round(channel_score, 4) if channel_score is not None else None,
                "platform_evidence_score": round(platform_evidence_score, 4),
                "evidence_confidence_score": round(evidence_confidence_score, 4),
                "platforms_observed": sorted(data["platforms"]),
                "notes": f"competition_bucket={competition_bucket}",
            }
        )
    return outputs


def main() -> None:
    if len(sys.argv) not in (2, 3):
        print("Usage: platform_evidence_to_candidates.py <platform_evidence.(csv|json)> [target_brand]", file=sys.stderr)
        sys.exit(1)

    rows = load_rows(sys.argv[1])
    target_brand = sys.argv[2] if len(sys.argv) == 3 else ""
    grouped = aggregate_rows(rows)

    if not grouped:
        print("No platform evidence rows found", file=sys.stderr)
        sys.exit(1)

    if not target_brand:
        target_brand = next(iter(grouped.keys()))
    if target_brand not in grouped:
        print(f"Target brand '{target_brand}' was not found in platform evidence data", file=sys.stderr)
        sys.exit(1)

    result = build_candidate_output(grouped, target_brand)
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
