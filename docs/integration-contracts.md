# Integration Contracts

## Tool-Semantics adapter

Expected input categories:

- Baseline and candidate interface snapshots
- Structural and semantic change report
- Probe results
- Model/tool-selection matrix
- Risk annotations

Recommended MER mapping:

- `change.change_type = tool_interface`
- `observations` contains change codes and probe outcomes
- `failure.failure_class = semantic_tool_drift` when behavior regresses
- linked reports are stored as artifact references

## MyelinMesh adapter

Expected input categories:

- Change set
- Selected scenarios and selection explanation
- Baseline/candidate metrics
- Release policy decision
- MCAP and simulation artifacts

Recommended MER mapping:

- `context.domain = physical_ai`
- `execution.scenario` names the physical test
- `observations` stores physical and operational metrics
- release decisions remain observations or tags, not proof of safety

## Parallax adapter

Expected input categories:

- Semantic trace
- Detection event
- Diagnosis candidates
- Recovery policy and result
- Post-recovery evaluation

Recommended MER mapping:

- `failure` represents detected runtime divergence
- `diagnosis` distinguishes evidence from hypotheses
- `recovery` records both successful and unsuccessful attempts

## Adapter contract

Adapters implement:

```python
class EvidenceAdapter(Protocol):
    name: str

    def can_handle(self, payload: dict[str, object]) -> bool: ...
    def convert(self, payload: dict[str, object]) -> list[EvidenceRecord]: ...
```

An adapter must not silently fabricate missing provenance. Unknown values should remain absent or explicitly unknown.
