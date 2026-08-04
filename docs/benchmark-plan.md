# Benchmark Plan

## Benchmark A — History-aware Physical AI test selection

Evaluate whether historical evidence improves scenario selection.

Inputs:

- Repository changes
- Capability graph
- Scenario registry
- Prior test results and incidents

Baselines:

- Full suite
- Random
- File heuristic
- Graph only
- Historical similarity only
- Combined MyelinMesh evidence

Metrics:

- Critical regression recall
- Overall regression recall
- Risk-weighted coverage
- Simulation time reduction
- False-negative rate

## Benchmark B — Usage-weighted tool compatibility

Evaluate whether trajectory history improves change severity ranking.

Metrics:

- Tool-selection regression recall
- Argument regression recall
- Affected-trajectory precision
- False escalation rate

## Benchmark C — Incident and recovery retrieval

Evaluate retrieval of relevant prior incidents without leaking exact duplicates.

Metrics:

- Recall@k
- Mean reciprocal rank
- Applicability precision
- Stale-evidence rejection
- Human usefulness rating

## Reproducibility

Each benchmark release should publish:

- Immutable dataset snapshot
- Train/validation/test split hashes
- Baseline implementations
- Environment lock file
- Evaluation script
- Error analysis
- Limitations and data card
