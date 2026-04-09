#!/usr/bin/env python3
import csv
import json
import os
import sys
from typing import Any, Dict, List, Tuple


PLACEHOLDER = "TBD"


def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_metadata(path: str) -> List[Dict[str, Any]]:
    lower = path.lower()
    if lower.endswith(".json"):
        payload = load_json(path)
        if isinstance(payload, list):
            return [row for row in payload if isinstance(row, dict)]
        if isinstance(payload, dict) and isinstance(payload.get("candidates"), list):
            return [row for row in payload["candidates"] if isinstance(row, dict)]
        raise ValueError("candidate metadata JSON must be a list of objects or an object with a candidates array")

    if lower.endswith(".csv"):
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return [dict(row) for row in reader]

    raise ValueError("candidate metadata must be .json or .csv")


def ensure_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def stringify(value: Any, default: str = "") -> str:
    if value is None:
        return default
    if isinstance(value, str):
        text = value.strip()
        return text if text else default
    return str(value)


def split_points(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [stringify(item) for item in value if stringify(item)]
    text = stringify(value)
    if not text:
        return []
    separators = ["\n", ";", "|", "、"]
    items = [text]
    for sep in separators:
        next_items: List[str] = []
        for item in items:
            next_items.extend(item.split(sep))
        items = next_items
    cleaned = [item.strip(" -•\t") for item in items if item.strip(" -•\t")]
    return cleaned


def candidate_key(name: str) -> str:
    return stringify(name).strip().casefold()


def index_metadata(rows: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    index: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        name = stringify(row.get("candidate") or row.get("name") or row.get("brand") or row.get("company"))
        if not name:
            continue
        index[candidate_key(name)] = row
    return index


def dedupe_keep_order(items: List[str]) -> List[str]:
    seen = set()
    result = []
    for item in items:
        key = candidate_key(item)
        if not key or key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def merge_candidate(ranking_row: Dict[str, Any], metadata_row: Dict[str, Any], index: int) -> Dict[str, Any]:
    name = stringify(ranking_row.get("candidate") or metadata_row.get("candidate") or metadata_row.get("name") or f"Candidate {index}", default=f"Candidate {index}")
    metadata_evidence = split_points(
        metadata_row.get("major_evidence_points")
        or metadata_row.get("evidence_points")
        or metadata_row.get("evidence")
        or metadata_row.get("notes")
    )
    metadata_uncertainty = split_points(
        metadata_row.get("major_uncertainty_points")
        or metadata_row.get("uncertainty_points")
        or metadata_row.get("uncertainties")
    )
    ranking_uncertainty = [stringify(item) for item in ensure_list(ranking_row.get("missing_metrics"))]
    ranking_uncertainty.extend(stringify(item) for item in ensure_list(ranking_row.get("warnings")))

    competitor_type = stringify(
        metadata_row.get("competitor_type")
        or metadata_row.get("type")
        or ranking_row.get("competitor_type"),
        default=PLACEHOLDER,
    )
    inclusion_reason = stringify(
        metadata_row.get("inclusion_reason")
        or ranking_row.get("inclusion_reason")
        or metadata_row.get("reason"),
        default=PLACEHOLDER,
    )
    score_logic = stringify(
        ranking_row.get("score_or_ranking_logic")
        or metadata_row.get("score_or_ranking_logic")
        or metadata_row.get("ranking_logic")
        or metadata_row.get("score_summary")
        or f"Coverage ratio {ranking_row.get('coverage_ratio', 'TBD')}; confidence {ranking_row.get('confidence', 'TBD')}",
        default=PLACEHOLDER,
    )

    merged = {
        "name": name,
        "rank": ranking_row.get("rank", metadata_row.get("rank", index)),
        "total_score": ranking_row.get("total_score", metadata_row.get("total_score")),
        "competitor_type": competitor_type,
        "inclusion_reason": inclusion_reason,
        "major_evidence_points": metadata_evidence,
        "major_uncertainty_points": dedupe_keep_order(metadata_uncertainty + ranking_uncertainty),
        "score_or_ranking_logic": score_logic,
        "confidence": ranking_row.get("confidence", metadata_row.get("confidence")),
        "coverage_ratio": ranking_row.get("coverage_ratio", metadata_row.get("coverage_ratio")),
    }

    for field in [
        "competition_bucket",
        "style_overlap_score",
        "age_overlap_score",
        "price_fit_score",
        "content_overlap_score",
        "channel_fit_score",
        "platform_evidence_score",
        "evidence_confidence_score",
        "platforms_observed",
    ]:
        if metadata_row.get(field) is not None and metadata_row.get(field) != "":
            merged[field] = metadata_row.get(field)

    sources = []
    if metadata_evidence:
        sources.append("candidate-metadata")
    if metadata_row.get("platforms_observed"):
        sources.append("platform-evidence")
    if ranking_row.get("breakdown"):
        sources.append("ranking-payload")
    if sources:
        merged["evidence_sources"] = dedupe_keep_order(sources)

    return merged


def derive_global_fields(base: Dict[str, Any], ranking_payload: Dict[str, Any]) -> Dict[str, Any]:
    warnings = [stringify(item) for item in ensure_list(ranking_payload.get("warnings")) if stringify(item)]
    recommendation = stringify(ranking_payload.get("recommendation"))
    overall_confidence = stringify(ranking_payload.get("overall_confidence"))

    derived: Dict[str, Any] = {}
    if "overall_confidence" not in base and overall_confidence:
        derived["overall_confidence"] = overall_confidence
    if "score_logic_summary" not in base and recommendation:
        derived["score_logic_summary"] = recommendation
    if "evidence_quality_note" not in base and warnings:
        derived["evidence_quality_note"] = "; ".join(warnings)
    if "main_caveats" not in base and warnings:
        derived["main_caveats"] = "; ".join(warnings)
    if recommendation == "qualitative-fallback-recommended" and "why_quantitative_ranking_was_not_used" not in base:
        derived["why_quantitative_ranking_was_not_used"] = "Quantitative ranking was not used because the remaining metrics were too sparse or too weakly discriminative to support a defensible score."
    return derived


def main() -> None:
    if len(sys.argv) != 4:
        print("Usage: merge_report_input.py <base_report.json> <ranking.json> <candidate_metadata.(json|csv)>", file=sys.stderr)
        sys.exit(1)

    base = load_json(sys.argv[1])
    ranking_payload = load_json(sys.argv[2])
    metadata_rows = load_metadata(sys.argv[3])

    if not isinstance(base, dict):
        print("base_report.json must be a JSON object", file=sys.stderr)
        sys.exit(1)
    if not isinstance(ranking_payload, dict) or not isinstance(ranking_payload.get("rankings"), list):
        print("ranking.json must be a JSON object with a rankings array", file=sys.stderr)
        sys.exit(1)

    metadata_index = index_metadata(metadata_rows)
    shortlist_details: List[Dict[str, Any]] = []
    for index, ranking_row in enumerate(ranking_payload["rankings"], start=1):
        if not isinstance(ranking_row, dict):
            print("ranking rows must be JSON objects", file=sys.stderr)
            sys.exit(1)
        key = candidate_key(ranking_row.get("candidate", ""))
        metadata_row = metadata_index.get(key, {})
        shortlist_details.append(merge_candidate(ranking_row, metadata_row, index))

    merged = dict(base)
    merged.update(derive_global_fields(base, ranking_payload))
    merged["ranking_payload"] = ranking_payload
    merged["shortlist_details"] = shortlist_details

    json.dump(merged, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
