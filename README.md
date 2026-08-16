# Agent Evaluation

> A reproducible framework for measuring AI agent behavior.

Agent Evaluation turns agent runs into evidence. It brings datasets, evaluators, metrics, judges, runners, traces, reports, and dashboards into one workflow so changes can be compared instead of merely demonstrated.

## First implemented contract

[Agent Trace Schema v0.1.0](traces/schema/v0.1.0/trace.schema.json) defines the
event stream emitted by the first executable
[Agent Harness vehicle demo](https://github.com/tinaxiaxiao/agent-harness/tree/main/examples/in_car_restaurant_agent).
It covers runtime lifecycle, input, planning, state changes, tool calls,
confirmation gates, side effects, outputs, completion, and privacy labels.

```bash
python3 -m unittest discover -s tests -v
```

The included validator has no third-party runtime dependencies.

## Why this repository exists

Agent systems fail in ways that single-answer benchmarks often miss: they choose the wrong tool, lose context, repeat work, stop too early, or reach the right answer through an unsafe path. Evaluation should therefore inspect both outcomes and trajectories.

## Architecture

```text
agent-evaluation/
├── datasets/      # Tasks, fixtures, expected outcomes, and dataset cards
├── evaluators/    # Deterministic, model-based, and human evaluation logic
├── metrics/       # Quality, reliability, latency, cost, and safety metrics
├── judges/        # Judge prompts, rubrics, calibration, and agreement checks
├── runners/       # Experiment execution and comparison workflows
├── traces/        # Trace schema, ingestion, normalization, and replay
├── reports/       # Reproducible summaries and regression reports
├── dashboard/     # Interactive exploration of runs and failures
└── design-notes/  # Evaluation methodology and design decisions
```

## Evaluation layers

1. **Outcome:** Did the agent complete the task correctly?
2. **Trajectory:** Were planning, tool use, and recovery appropriate?
3. **System:** What did the run cost in time, tokens, and external actions?
4. **Reliability:** Does the result hold across repetitions and environments?

## Design principles

- **Reproducible:** datasets, configurations, and versions travel with results.
- **Trace-first:** final answers and intermediate behavior are both measurable.
- **Calibrated:** model judges are tested against deterministic and human signals.
- **Comparable:** every report makes the baseline and change explicit.
- **Actionable:** failures map back to components that can be improved.

## Roadmap

- [x] Define a versioned trace schema
- [ ] Define a versioned task schema
- [ ] Ship deterministic evaluators and a local runner
- [ ] Add judge rubrics with calibration examples
- [ ] Generate a first regression report
- [ ] Add trace exploration to the dashboard

## Relationship to Agent Harness

Agent Evaluation is runtime-agnostic, but [**Agent Harness**](https://github.com/tinaxiaxiao/agent-harness) is the reference producer for its trace format and the first integration used to validate the full loop.

## Status

Early design and scaffolding. The first milestone is one small dataset evaluated end to end with a reproducible report.
