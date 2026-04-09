#!/usr/bin/env python3
import json
import math
import sys
from typing import Any, Dict, List, Tuple


def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def normalize_weights(weights: Dict[str, Any]) -> Tuple[Dict[str, float], float, List[str]]:
    if not isinstance(weights, dict) or not weights:
        raise ValueError("weights.json must be a non-empty JSON object")

    validated: Dict[str, float] = {}
    for metric, weight in weights.items():
        if not is_number(weight):
            raise ValueError(f"Weight for metric '{metric}' must be numeric")
        weight_value = float(weight)
        if weight_value < 0:
            raise ValueError(f"Weight for metric '{metric}' cannot be negative")
        validated[metric] = weight_value

    weight_sum = sum(validated.values())
    if math.isclose(weight_sum, 0.0):
        raise ValueError("Weight sum must be greater than zero")

    normalized = {metric: value / weight_sum for metric, value in validated.items()}
    warnings: List[str] = []
    if not math.isclose(weight_sum, 1.0, rel_tol=1e-9, abs_tol=1e-9):
        warnings.append(
            f"Input weights summed to {round(weight_sum, 6)}; normalized automatically to 1.0 for comparable total scores."
        )
    return normalized, weight_sum, warnings


def candidate_confidence(coverage_ratio: float) -> str:
    if coverage_ratio >= 0.8:
        return "high"
    if coverage_ratio >= 0.5:
        return "medium"
    return "low"


def extract_scores_payload(payload: Any) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    if isinstance(payload, list):
        return payload, {}
    if isinstance(payload, dict) and isinstance(payload.get("normalized_scores"), list):
        normalization_summary = payload.get("normalization_summary")
        if normalization_summary is None:
            normalization_summary = {}
        if not isinstance(normalization_summary, dict):
            raise ValueError("normalization_summary must be a JSON object when provided")
        return payload["normalized_scores"], normalization_summary
    raise ValueError("scores.json must be either a JSON array or an object with normalized_scores")


def overall_confidence_from_recommendation(recommendation: str) -> str:
    if recommendation == "quantitative-ranking-ok":
        return "high"
    if recommendation == "quantitative-ranking-low-confidence":
        return "medium"
    return "low"


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: weighted_rank.py <scores.json> <weights.json>", file=sys.stderr)
        sys.exit(1)

    scores_payload = load_json(sys.argv[1])
    weights = load_json(sys.argv[2])

    try:
        scores, normalization_summary = extract_scores_payload(scores_payload)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)

    if not isinstance(scores, list):
        print("scores.json must resolve to a JSON array of score rows", file=sys.stderr)
        sys.exit(1)

    try:
        normalized_weights, input_weight_sum, warnings = normalize_weights(weights)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)

    metrics = list(normalized_weights.keys())
    if len(metrics) < 2:
        warnings.append("Fewer than two weighted metrics were provided; qualitative fallback is usually safer.")
    if len(scores) < 2:
        warnings.append("Fewer than two candidates were provided; ranking is not meaningful.")

    normalization_recommendation = normalization_summary.get("recommendation")
    normalization_warnings = normalization_summary.get("warnings", [])
    if not isinstance(normalization_warnings, list):
        print("normalization_summary.warnings must be a JSON array", file=sys.stderr)
        sys.exit(1)
    warnings.extend(str(item) for item in normalization_warnings)

    rankings: List[Dict[str, Any]] = []
    coverage_ratios: List[float] = []

    for row in scores:
        if not isinstance(row, dict):
            print("Each score row must be a JSON object", file=sys.stderr)
            sys.exit(1)

        total = 0.0
        breakdown: Dict[str, float] = {}
        missing: List[str] = []
        row_warnings: List[str] = []
        available_metrics = 0

        for metric, weight in normalized_weights.items():
            value = row.get(metric)
            if value is None:
                missing.append(metric)
                continue
            if not is_number(value):
                missing.append(metric)
                row_warnings.append(f"Metric '{metric}' is non-numeric and was ignored.")
                continue

            available_metrics += 1
            contribution = float(value) * float(weight)
            breakdown[metric] = round(contribution, 6)
            total += contribution

        coverage_ratio = available_metrics / len(metrics) if metrics else 0.0
        coverage_ratios.append(coverage_ratio)
        confidence = candidate_confidence(coverage_ratio)

        if coverage_ratio < 0.5:
            row_warnings.append("Sparse metric coverage for this candidate; qualitative interpretation is safer.")
        elif coverage_ratio < 0.8:
            row_warnings.append("Some weighted metrics are missing; treat ranking confidence as medium.")

        rankings.append(
            {
                "candidate": row.get("candidate", "unknown"),
                "total_score": round(total, 4),
                "breakdown": breakdown,
                "missing_metrics": missing,
                "coverage_ratio": round(coverage_ratio, 3),
                "confidence": confidence,
                "warnings": row_warnings,
            }
        )

    rankings.sort(key=lambda x: x["total_score"], reverse=True)
    for i, row in enumerate(rankings, start=1):
        row["rank"] = i

    average_coverage = sum(coverage_ratios) / len(coverage_ratios) if coverage_ratios else 0.0
    if average_coverage < 0.6:
        warnings.append("Average weighted metric coverage is below 0.6; qualitative fallback is recommended.")

    if (
        len(scores) < 2
        or len(metrics) < 2
        or average_coverage < 0.6
        or normalization_recommendation == "qualitative-fallback-recommended"
    ):
        recommendation = "qualitative-fallback-recommended"
    elif (
        any(row["confidence"] == "low" for row in rankings)
        or normalization_recommendation == "normalization-low-confidence"
    ):
        recommendation = "quantitative-ranking-low-confidence"
    else:
        recommendation = "quantitative-ranking-ok"

    result = {
        "rankings": rankings,
        "weight_summary": {
            "input_weight_sum": round(input_weight_sum, 6),
            "normalized_weights": {metric: round(value, 6) for metric, value in normalized_weights.items()},
        },
        "coverage_summary": {
            "candidate_count": len(scores),
            "metric_count": len(metrics),
            "average_coverage_ratio": round(average_coverage, 3),
        },
        "normalization_summary": normalization_summary,
        "recommendation": recommendation,
        "overall_confidence": overall_confidence_from_recommendation(recommendation),
        "warnings": warnings,
    }

    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
