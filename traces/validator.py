"""Dependency-free validator for Agent Trace JSONL files.

The JSON Schema is the normative contract. This small validator covers the
contract's current constraints so examples and CI can run with Python alone.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


SCHEMA_PATH = Path(__file__).parent / "schema" / "v0.1.0" / "trace.schema.json"


class TraceValidationError(ValueError):
    """Raised when an event violates the trace contract."""


def load_contract() -> dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def validate_event(event: dict[str, Any], contract: dict[str, Any] | None = None) -> None:
    contract = contract or load_contract()
    required = set(contract["required"])
    missing = sorted(required - event.keys())
    if missing:
        raise TraceValidationError(f"missing required fields: {', '.join(missing)}")

    extra = sorted(set(event) - set(contract["properties"]))
    if extra and contract.get("additionalProperties") is False:
        raise TraceValidationError(f"unexpected fields: {', '.join(extra)}")

    if event["schema_version"] != contract["properties"]["schema_version"]["const"]:
        raise TraceValidationError("unsupported schema_version")
    if not isinstance(event["sequence"], int) or event["sequence"] < 1:
        raise TraceValidationError("sequence must be a positive integer")
    if not isinstance(event["duration_ms"], int) or event["duration_ms"] < 0:
        raise TraceValidationError("duration_ms must be a non-negative integer")

    for field in ("event_id", "trace_id", "run_id", "component"):
        if not isinstance(event[field], str) or not event[field]:
            raise TraceValidationError(f"{field} must be a non-empty string")

    try:
        datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00"))
    except (AttributeError, ValueError) as exc:
        raise TraceValidationError("timestamp must be ISO 8601 date-time") from exc

    event_types = contract["properties"]["event_type"]["enum"]
    if event["event_type"] not in event_types:
        raise TraceValidationError(f"unknown event_type: {event['event_type']}")
    statuses = contract["properties"]["status"]["enum"]
    if event["status"] not in statuses:
        raise TraceValidationError(f"unknown status: {event['status']}")
    if not isinstance(event["attributes"], dict):
        raise TraceValidationError("attributes must be an object")

    privacy = event["privacy"]
    if not isinstance(privacy, dict) or set(privacy) != {"classification", "redacted"}:
        raise TraceValidationError("privacy must contain classification and redacted")
    classes = contract["properties"]["privacy"]["properties"]["classification"]["enum"]
    if privacy["classification"] not in classes or not isinstance(privacy["redacted"], bool):
        raise TraceValidationError("invalid privacy declaration")


def validate_events(events: Iterable[dict[str, Any]]) -> int:
    contract = load_contract()
    expected_sequence = 1
    trace_identity: tuple[str, str] | None = None
    count = 0
    for event in events:
        validate_event(event, contract)
        identity = (event["trace_id"], event["run_id"])
        if trace_identity is None:
            trace_identity = identity
        elif identity != trace_identity:
            raise TraceValidationError("all events must share trace_id and run_id")
        if event["sequence"] != expected_sequence:
            raise TraceValidationError(
                f"expected sequence {expected_sequence}, got {event['sequence']}"
            )
        expected_sequence += 1
        count += 1
    if count == 0:
        raise TraceValidationError("trace is empty")
    return count


def validate_jsonl(path: str | Path) -> int:
    source = Path(path)
    events = []
    for line_number, line in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise TraceValidationError(f"line {line_number}: invalid JSON") from exc
    return validate_events(events)
