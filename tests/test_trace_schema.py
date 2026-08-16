import unittest

from traces.validator import TraceValidationError, validate_event, validate_events


def valid_event(sequence: int = 1) -> dict:
    return {
        "schema_version": "0.1.0",
        "event_id": f"event_{sequence:04d}",
        "trace_id": "trace_test",
        "run_id": "run_test",
        "sequence": sequence,
        "timestamp": "2026-08-16T12:00:00.000Z",
        "event_type": "run.started",
        "component": "runtime",
        "status": "started",
        "duration_ms": 0,
        "parent_event_id": None,
        "side_effect": False,
        "attributes": {},
        "privacy": {"classification": "synthetic", "redacted": True},
    }


class TraceSchemaTests(unittest.TestCase):
    def test_valid_event(self) -> None:
        validate_event(valid_event())

    def test_missing_field_is_rejected(self) -> None:
        event = valid_event()
        del event["privacy"]
        with self.assertRaisesRegex(TraceValidationError, "missing required"):
            validate_event(event)

    def test_unknown_event_type_is_rejected(self) -> None:
        event = valid_event()
        event["event_type"] = "model.did_magic"
        with self.assertRaisesRegex(TraceValidationError, "unknown event_type"):
            validate_event(event)

    def test_non_contiguous_sequence_is_rejected(self) -> None:
        with self.assertRaisesRegex(TraceValidationError, "expected sequence 2"):
            validate_events([valid_event(1), valid_event(3)])

    def test_mixed_runs_are_rejected(self) -> None:
        second = valid_event(2)
        second["run_id"] = "different_run"
        with self.assertRaisesRegex(TraceValidationError, "share trace_id and run_id"):
            validate_events([valid_event(1), second])


if __name__ == "__main__":
    unittest.main()
