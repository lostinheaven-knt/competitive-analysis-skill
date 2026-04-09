#!/usr/bin/env python3
import json
import sys
from typing import Any, Dict, List, Tuple


PLACEHOLDER = "TBD"


def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def ensure_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def stringify(value: Any, default: str = PLACEHOLDER) -> str:
    if value is None:
        return default
    if isinstance(value, str):
        text = value.strip()
        return text if text else default
    return str(value)


def bullet_list(items: List[Any], fallback: str = "- None yet") -> str:
    cleaned = [stringify(item, default="").strip() for item in ensure_list(items)]
    cleaned = [item for item in cleaned if item]
    if not cleaned:
        return fallback
    return "\n".join(f"- {item}" for item in cleaned)


def get_first(data: Dict[str, Any], *keys: str, default: Any = None) -> Any:
    for key in keys:
        if key in data and data.get(key) is not None:
            return data.get(key)
    return default


def candidate_name(candidate: Dict[str, Any], index: int) -> str:
    return stringify(
        get_first(candidate, "name", "candidate", "company_name", "brand_name", default=f"Candidate {index}"),
        default=f"Candidate {index}",
    )


def map_ranking_to_candidate(row: Dict[str, Any], index: int) -> Dict[str, Any]:
    missing_metrics = ensure_list(row.get("missing_metrics"))
    candidate_warnings = ensure_list(row.get("warnings"))
    warning_items = missing_metrics + candidate_warnings
    return {
        "name": row.get("candidate", f"Candidate {index}"),
        "rank": row.get("rank", index),
        "total_score": row.get("total_score"),
        "competitor_type": row.get("competitor_type", "TBD"),
        "inclusion_reason": row.get("inclusion_reason", "TBD"),
        "major_evidence_points": ensure_list(row.get("major_evidence_points")),
        "major_uncertainty_points": warning_items,
        "score_or_ranking_logic": row.get(
            "score_or_ranking_logic",
            f"Coverage ratio {row.get('coverage_ratio', 'TBD')}; confidence {row.get('confidence', 'TBD')}",
        ),
    }


def normalize_candidates(data: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    raw_candidates = get_first(data, "shortlist_details", "candidates", "final_shortlist", default=None)
    if raw_candidates is not None:
        normalized: List[Dict[str, Any]] = []
        for index, item in enumerate(ensure_list(raw_candidates), start=1):
            if isinstance(item, dict):
                candidate = dict(item)
            else:
                candidate = {"name": stringify(item, default=f"Candidate {index}")}
            if "rank" not in candidate:
                candidate["rank"] = index
            normalized.append(candidate)
        return normalized, {}

    ranking_payload = data.get("ranking_payload")
    if isinstance(ranking_payload, dict) and isinstance(ranking_payload.get("rankings"), list):
        candidates = [map_ranking_to_candidate(item, index) for index, item in enumerate(ranking_payload["rankings"], start=1)]
        derived = {
            "overall_confidence": ranking_payload.get("overall_confidence"),
            "score_logic_summary": ranking_payload.get("recommendation"),
            "evidence_quality_note": "; ".join(str(item) for item in ensure_list(ranking_payload.get("warnings"))) or None,
            "main_caveats": "; ".join(str(item) for item in ensure_list(ranking_payload.get("warnings"))) or None,
        }
        return candidates, derived

    raw_candidates = data.get("shortlist", [])
    if raw_candidates is None:
        raw_candidates = data.get("shortlist", [])

    normalized: List[Dict[str, Any]] = []
    for index, item in enumerate(ensure_list(raw_candidates), start=1):
        if isinstance(item, dict):
            candidate = dict(item)
        else:
            candidate = {"name": stringify(item, default=f"Candidate {index}")}
        if "rank" not in candidate:
            candidate["rank"] = index
        normalized.append(candidate)
    return normalized, {}


def shortlist_overview(candidates: List[Dict[str, Any]]) -> str:
    if not candidates:
        return "- None yet"

    lines = []
    for index, candidate in enumerate(candidates, start=1):
        name = candidate_name(candidate, index)
        competitor_type = stringify(get_first(candidate, "competitor_type", "type"))
        inclusion_reason = stringify(candidate.get("inclusion_reason"))
        lines.append(f"- {name} ({competitor_type}) — {inclusion_reason}")
    return "\n".join(lines)


def render_candidate_cards(candidates: List[Dict[str, Any]]) -> str:
    if not candidates:
        return "## Candidate 1\n- Name: TBD\n- Competitor type: TBD\n- Inclusion reason: TBD\n- Major evidence points:\n  - TBD\n- Major uncertainty points:\n  - TBD\n- Score or ranking logic: TBD\n- Rank / total score: TBD\n"

    cards: List[str] = []
    for index, candidate in enumerate(candidates, start=1):
        name = candidate_name(candidate, index)
        competitor_type = stringify(get_first(candidate, "competitor_type", "type"))
        inclusion_reason = stringify(candidate.get("inclusion_reason"))
        evidence_points = bullet_list(get_first(candidate, "major_evidence_points", "evidence_points", default=[]), fallback="- TBD")
        uncertainty_points = bullet_list(get_first(candidate, "major_uncertainty_points", "uncertainty_points", default=[]), fallback="- TBD")
        ranking_logic = stringify(get_first(candidate, "score_or_ranking_logic", "ranking_logic", "score_summary"))
        rank_value = stringify(candidate.get("rank"))
        total_score = stringify(candidate.get("total_score"))
        cards.append(
            f"## {index}. {name}\n"
            f"- Name: {name}\n"
            f"- Competitor type: {competitor_type}\n"
            f"- Inclusion reason: {inclusion_reason}\n"
            f"- Major evidence points:\n{evidence_points}\n"
            f"- Major uncertainty points:\n{uncertainty_points}\n"
            f"- Score or ranking logic: {ranking_logic}\n"
            f"- Rank / total score: rank {rank_value} / {total_score}"
        )
    return "\n\n".join(cards)


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: generate_report_outline.py <input.json>", file=sys.stderr)
        sys.exit(1)

    data = load_json(sys.argv[1])
    if not isinstance(data, dict):
        print("input.json must be a JSON object", file=sys.stderr)
        sys.exit(1)

    candidates, derived = normalize_candidates(data)
    shortlist_names = [candidate_name(candidate, index) for index, candidate in enumerate(candidates, start=1)]

    md = f"""# Executive Summary
- Objective: {stringify(data.get('objective'))}
- Scope: {stringify(data.get('scope'))}
- Final shortlist: {', '.join(shortlist_names) if shortlist_names else PLACEHOLDER}
- Main caveats: {stringify(get_first(data, 'main_caveats', default=derived.get('main_caveats')))}
- Overall confidence: {stringify(get_first(data, 'overall_confidence', default=derived.get('overall_confidence')))}

# Scope and Assumptions
- Target: {stringify(data.get('target'))}
- Industry: {stringify(data.get('industry'))}
- Region: {stringify(data.get('region'))}
- Customer: {stringify(data.get('target_customer'))}
- Channel: {stringify(data.get('channel'))}
- Price band: {stringify(data.get('price_band'))}
- Time horizon: {stringify(data.get('time_horizon'))}
- Key assumptions: {stringify(data.get('key_assumptions'))}

# Sources and Evidence Quality
- Primary sources: {stringify(data.get('primary_sources'))}
- Secondary sources: {stringify(data.get('secondary_sources'))}
- Weak or conflicting evidence: {stringify(data.get('weak_evidence'))}
- Evidence quality note: {stringify(get_first(data, 'evidence_quality_note', default=derived.get('evidence_quality_note')))}

# Candidate Pool
- Candidate count: {stringify(data.get('candidate_count'))}
- Inclusion logic: {stringify(data.get('inclusion_logic'))}
- Excluded categories: {stringify(data.get('excluded_categories'))}
- Watchlist or secondary players: {stringify(data.get('watchlist'))}

# Method and Weighting
- Framework used: {stringify(data.get('framework_used'))}
- Weight preset: {stringify(data.get('weight_preset'))}
- Any custom adjustments: {stringify(data.get('custom_adjustments'), default='None')}
- Score or ranking logic summary: {stringify(get_first(data, 'score_logic_summary', default=derived.get('score_logic_summary')))}

# Final Shortlist Overview
{shortlist_overview(candidates)}

# Competitor Detail Cards
{render_candidate_cards(candidates)}

# Key Findings
{bullet_list(data.get('key_findings'))}

# Risks and Limitations
{bullet_list(data.get('risks'))}

# Recommended Next Steps
{bullet_list(data.get('next_steps'))}
"""
    sys.stdout.write(md)


if __name__ == "__main__":
    main()
