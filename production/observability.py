"""Observability -- turn agent_pro's event stream into metrics + OTel-style spans.

agent_pro emits structured events (model_reply, tool_use, tool_result, guardrail_flag,
...). This module summarizes a run for dashboards/logs and exports spans you could ship
to OpenTelemetry. Pure functions over a Result; no I/O, no key.
"""
import json


def summarize(result) -> dict:
    ev = result.events
    return {
        "steps": result.usage.steps,
        "tool_calls": sum(1 for e in ev if e["kind"] == "tool_use"),
        "tool_errors": sum(1 for e in ev if e["kind"] == "tool_result" and e.get("is_error")),
        "blocked": sum(1 for e in ev if e["kind"] == "tool_blocked"),
        "guardrail_flags": sum(1 for e in ev if e["kind"] == "guardrail_flag"),
        "input_tokens": result.usage.input_tokens,
        "output_tokens": result.usage.output_tokens,
        "cost_usd": round(result.usage.cost_usd, 6),
        "duration_ms": ev[-1]["t_ms"] if ev else 0,
        "stop_reason": result.stop_reason,
    }


def spans(result) -> list:
    """One span per event (OTel-ish): name + relative timestamp + attributes."""
    return [{"name": e["kind"], "t_ms": e["t_ms"],
             "attrs": {k: v for k, v in e.items() if k not in ("kind", "t_ms")}}
            for e in result.events]


def to_otel_json(result) -> str:
    return json.dumps({"metrics": summarize(result), "spans": spans(result)}, indent=2)
