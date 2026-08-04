# Research Agenda

MyelinMesh is a product-oriented open-source project with a research program. The research contribution is not merely storing traces; it is studying how heterogeneous evidence should be represented, selected, reused, and invalidated.

## RQ1 — History-aware test selection

Can prior incidents, test yield, and capability dependencies reduce Physical AI simulation cost without reducing critical regression recall?

Baselines:

- Full test suite
- Random selection
- File-path heuristic
- Dependency-graph selection
- Historical-similarity selection
- Graph + history + risk selection

Primary metrics:

- Critical regression recall
- Risk-weighted coverage
- Simulation reduction
- False-negative rate
- Runtime cost

## RQ2 — Usage-weighted interface compatibility

Can historical agent trajectories distinguish operationally important tool changes from technically breaking but rarely relevant changes?

Primary metrics:

- Tool-selection regression recall
- Argument-validity regression recall
- Affected-trajectory coverage
- False escalation rate

## RQ3 — Cross-layer failure representation

Can agent and Physical AI failures share a representation based on expectation, action, observation, divergence, risk, and recovery?

Study domains:

- MCP tool semantic drift
- Retrieval and memory staleness
- Robot perception latency
- Sensor and transform degradation
- Recovery outcomes

## RQ4 — Active evidence acquisition

Given multiple plausible hypotheses, which next test most reduces uncertainty while respecting cost and safety constraints?

Candidate methods:

- Expected information gain
- Bayesian experimental design
- Boundary-focused scenario sampling
- Risk-constrained active learning

## RQ5 — Recovery transfer and decay

When may recovery evidence be reused across software versions, robot platforms, models, or environments? How should confidence decay after relevant changes?

## Scientific guardrails

- Similarity is not causality.
- Human labels are not automatically ground truth.
- Synthetic and real evidence must remain distinguishable.
- Training and evaluation incidents must be separated to prevent leakage.
- Negative and unsuccessful outcomes must be retained.
- Claims must include uncertainty and applicability conditions.
