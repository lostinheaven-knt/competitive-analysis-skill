#!/usr/bin/env python3
import json
import math
import sys
from typing import Any, Dict, List, Tuple

NON_METRIC_FIELDS = {"candidate", "notes", "confidence", "type"}


def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def min_max(values: List[float], reverse: bool = False) -> List[float]:
    low = min(values)
    high = max(values)
    scores = [(v - low) / (high - low) for v in values]
    if reverse:
        scores = [1.0 - s for s in scores]
    return scores


def rank_based(values: List[float], reverse: bool = False) -> List[float]:
    order = sorted(enumerate(values), key=lambda x: x[1], reverse=not reverse)
    if len(values) == 1:
        return [1.0]
    result = [0.0] * len(values)
    for rank, (idx, _) in enumerate(order):
        result[idx] = 1.0 - rank / (len(values) - 1)
    return result


def metric_status(values: List[float]) -> str:
    if len(values) < 2:
        return "insufficient-data"
    if math.isclose(min(values), max(values)):
        return "no-variance"
    return "ok"


def normalize_metric(values: List[float], method: str, reverse: bool) -> Tuple[List[float], str]:
    status = metric_status(values)
    if status == "insufficient-data":
        return [], status
    if status == "no-variance":
        return [0.5 for _ in values], status
    if method == "rank":
        return rank_based(values, reverse=reverse), status
    return min_max(values, reverse=reverse), status


def normalize(rows: List[Dict[str, Any]], directions: Dict[str, str], method: str) -> Dict[str, Any]:
    metrics = set()
    for row in rows:
        for key, value in row.items():
            if key not in NON_METRIC_FIELDS and is_number(value):
                metrics.add(key)

    output = [{"candidate": row.get("candidate", "unknown")} for row in rows]
    metric_summaries: List[Dict[str, Any]] = []
    warnings: List[str] = []
    low_information_metrics = 0

    for metric in sorted(metrics):
        indexed_values = [(i, row.get(metric)) for i, row in enumerate(rows) if is_number(row.get(metric))]
        positions = [i for i, _ in indexed_values]
        values = [float(v) for _, v in indexed_values]
        reverse = directions.get(metric) == "lower_is_better"
        missing_candidates = len(rows) - len(values)

        normalized_values, status = normalize_metric(values, method, reverse)
        metric_warning = None
        if status == "insufficient-data":
            low_information_metrics += 1
            metric_warning = f"Metric '{metric}' has fewer than two comparable numeric values; excluding it from quantitative ranking."
            warnings.append(metric_warning)
        elif status == "no-variance":
            low_information_metrics += 1
            metric_warning = f"Metric '{metric}' has no variance across comparable candidates; assigning neutral normalized scores and lowering confidence."
            warnings.append(metric_warning)

        if status == "insufficient-data":
            metric_result: Dict[int, Any] = {}
        else:
            metric_result = {idx: round(score, 6) for idx, score in zip(positions, normalized_values)}

        for idx, out in enumerate(output):
            out[metric] = metric_result.get(idx)

        metric_summaries.append(
            {
                "metric": metric,
                "status": status,
                "direction": directions.get(metric, "higher_is_better"),
                "comparable_candidates": len(values),
                "missing_candidates": missing_candidates,
                "warning": metric_warning,
            }
        )

    comparable_metrics = [m for m in metric_summaries if m["status"] == "ok"]
    if not metrics:
        warnings.append("No numeric metrics were found; qualitative fallback is required.")
        recommendation = "qualitative-fallback-recommended"
    elif len(comparable_metrics) < 2:
        warnings.append("Fewer than two discriminative metrics remain after normalization checks; qualitative fallback is recommended.")
        recommendation = "qualitative-fallback-recommended"
    elif low_information_metrics > len(metric_summaries) / 2:
        warnings.append("More than half of the weighted metrics are low-information; treat any ranking as low confidence.")
        recommendation = "qualitative-fallback-recommended"
    elif low_information_metrics > 0:
        recommendation = "normalization-low-confidence"
    else:
        recommendation = "normalization-ok"

    return {
        "normalized_scores": output,
        "normalization_summary": {
            "method": method,
            "metric_count": len(metric_summaries),
            "comparable_metric_count": len(comparable_metrics),
            "low_information_metric_count": low_information_metrics,
            "metrics": metric_summaries,
            "recommendation": recommendation,
            "warnings": warnings,
        },
    }


def main() -> None:
    if len(sys.argv) not in (2, 3, 4):
        print(
            "Usage: normalize_scores.py <scores.json> [directions.json] [minmax|rank]",
            file=sys.stderr,
        )
        sys.exit(1)

    scores_path = sys.argv[1]
    directions_path = sys.argv[2] if len(sys.argv) >= 3 and sys.argv[2].endswith(".json") else None
    method = sys.argv[3] if directions_path and len(sys.argv) == 4 else (sys.argv[2] if len(sys.argv) == 3 and not sys.argv[2].endswith(".json") else "minmax")

    if method not in {"minmax", "rank"}:
        print("Method must be one of: minmax, rank", file=sys.stderr)
        sys.exit(1)

    rows = load_json(scores_path)
    if not isinstance(rows, list):
        print("scores.json must be a JSON array", file=sys.stderr)
        sys.exit(1)

    directions = load_json(directions_path) if directions_path else {}
    if not isinstance(directions, dict):
        print("directions.json must be a JSON object", file=sys.stderr)
        sys.exit(1)

    result = normalize(rows, directions, method)
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
