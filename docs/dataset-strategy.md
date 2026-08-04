# Dataset Strategy

## Evidence categories

MyelinMesh should ingest and distinguish:

1. Code, configuration, model, prompt, and tool changes
2. Test and simulation history
3. Runtime incidents and physical telemetry
4. Agent and tool-use trajectories
5. Public benchmark or robotics datasets
6. Human review and operator judgments

## Dataset requirements

Every imported dataset should include a data card covering:

- Source and license
- Collection method
- Date and version
- Real, simulated, benchmark, or synthetic status
- Known missingness and bias
- Privacy and redistribution constraints
- Labeling process
- Recommended and prohibited uses

## Leakage prevention

Incidents used to train retrieval, ranking, or test-selection models must not appear in the evaluation split through duplicate traces, derived scenarios, or near-identical version variants.

## Negative evidence

The corpus must retain:

- Tests that found no issue
- Failed recovery attempts
- Incorrect diagnoses
- Human disagreement
- Non-reproduced incidents

Removing negative evidence would produce misleading confidence.

## Public-corpus roadmap

A future open corpus may package:

```text
change → selected test or intent → execution → observation → failure → recovery → outcome
```

Large raw artifacts should live in versioned object storage; MER records should reference immutable checksums and locations.
