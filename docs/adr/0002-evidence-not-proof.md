# ADR 0002: Represent evidence without claiming proof

- Status: Accepted
- Date: 2026-08-04

## Context

AI reliability systems can produce persuasive explanations that exceed the strength of the underlying data.

## Decision

The schema separates observations, hypotheses, confidence, provenance, validation, and human review. It does not provide a generic `root_cause_proven` flag.

## Consequences

- Consumers must express uncertainty.
- Causal claims require external experimental methods.
- Similar incident retrieval cannot directly authorize recovery or release decisions.
