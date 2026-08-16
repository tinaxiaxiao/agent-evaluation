# Traces

This directory owns the versioned event contract consumed by Agent Evaluation
and emitted by Agent Harness.

## Trace Schema v0.1.0

The canonical schema is [`schema/v0.1.0/trace.schema.json`](schema/v0.1.0/trace.schema.json).
Each line in a trace is one JSON event with a stable identity, contiguous
sequence number, timestamp, component, status, attributes, and privacy label.

The first contract covers runtime lifecycle, input, intent, planning, state
changes, tool calls, confirmation gates, side effects, outputs, and completion.

## Validate a trace

The validator uses only the Python standard library:

```bash
python -c 'from traces import validate_jsonl; print(validate_jsonl("trace.jsonl"))'
```

Run the contract tests with:

```bash
python -m unittest discover -s tests -v
```

## Privacy

Public traces must declare their data classification. The first vehicle demo
uses synthetic locations, restaurants, reservations, and user decisions; no
real coordinates or personal booking information are stored.
