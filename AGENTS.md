# AGENTS.md — Course of Action

This document turns the repository's SWOT analysis (single-maintainer bus
factor, no proven external adoption yet, an ambitious multi-milestone
roadmap) into concrete workstreams. Each is framed as an agent role with a
scope, the inputs/triggers that start it, and the criteria that close it.
Treat these as assignable units of work — for a human contributor, an AI
agent, or both — not as a prose wishlist.

## 1. Adoption/Validation Agent

**Addresses:** no proven external usage yet; `PROJECT_CHARTER.md`'s own
six-month success criteria (three external producers, 1,000 ingested
records, two external contributor adapters/datasets) are unmet.

- **Scope:** Get at least one real, external producer emitting valid MER
  records through the existing adapters — not another internal example.
- **Inputs/Triggers:** Runs now, in parallel with feature work; do not gate
  it behind v0.3 completion.
- **Done-criteria:** One external system's output round-trips through
  `myelinmesh validate` → `ingest` → `search`/`show` without hand-editing the
  adapter output. Record the result in `VALIDATION_REPORT.md` or a follow-up
  report.

## 2. Retrieval Delivery Agent

**Addresses:** work already in flight for v0.3.0 — Evidence retrieval.

- **Scope:** Land the open draft PRs and close their tracking issues before
  picking up new v0.3 scope: PR #43 (structured retrieval filters →
  issue #34), PR #44 (applicability filtering before ranking → issue #37),
  PR #45 (multi-agent engineering workflow), PR #46 (report-only consistency
  audit).
- **Inputs/Triggers:** CI green on each PR; no unmerged draft PR should sit
  longer than the next roadmap slice.
- **Done-criteria:** #43–#46 merged or explicitly closed with a reason;
  issues #34 and #37 closed; `ROADMAP.md`'s v0.3.0 checklist updated to match.

## 3. Infrastructure-Deferral Agent

**Addresses:** local-first storage limits future scale, but building
Postgres/pgvector ahead of demonstrated need is a diversion from validation.

- **Scope:** Explicitly hold issues #35 (optional PostgreSQL backend) and
  #36 (optional pgvector similarity index) — do not start implementation.
- **Inputs/Triggers:** Revisit only when one of: (a) the Adoption/Validation
  Agent's external producer needs multi-writer or > single-machine scale, or
  (b) local SQLite measurably fails at the record volumes actually being
  ingested.
- **Done-criteria:** A short note added to #35/#36 recording the trigger
  condition, so the decision to defer is visible rather than silent.

## 4. Contributor & Community Agent

**Addresses:** bus factor of 1 — every commit and both open PRs currently
come from a single author, against the charter's stated goal of external
contributors.

- **Scope:** Lower the barrier for a second contributor: label a small
  number of issues `good first issue` (a new adapter is the best fit, per
  `CONTRIBUTING.md`'s "Contribution areas"), and make sure
  `CONTRIBUTING.md`'s adapter-writing path is concrete enough to follow
  without asking the maintainer first.
- **Inputs/Triggers:** Can start immediately; does not block on other
  workstreams.
- **Done-criteria:** At least one PR merged from an author other than the
  project creator, or — short of that — a documented adapter-contribution
  template that a new contributor could follow unassisted.

## 5. Naming/Brand Resolution Agent

**Addresses:** `VALIDATION_REPORT.md` flags that the shorter name "Myelin" is
already used by an adjacent AI-agent project; the repo currently relies on
consistent use of the full "MyelinMesh" name as an informal mitigation.

- **Scope:** Decide, deliberately, whether "MyelinMesh" needs formal
  trademark/name clearance before more docs, dataset branding (v0.5.0), or a
  public package release commit further to the name.
- **Inputs/Triggers:** Before `docs/name-due-diligence.md` is treated as
  closed, and before the v0.5.0 "open reliability corpus" milestone begins
  (that milestone publishes datasets under the project name externally).
- **Done-criteria:** `docs/name-due-diligence.md` updated with either a
  clearance decision or an explicit acceptance of the risk, dated and
  reasoned.

## 6. Release & QA Agent

**Addresses:** the project's engineering hygiene (typed code, CI matrix,
86% coverage, CodeQL) is a genuine strength — the risk is regression as scope
grows into v0.4+.

- **Scope:** Keep `make lint`, `make typecheck`, `make test`, and the schema
  regeneration check green as the mandatory bar for every PR, including ones
  opened by external contributors (see Agent 4). No exceptions for
  "docs-only" PRs that touch `models.py` or the schema.
- **Inputs/Triggers:** Every PR, ongoing.
- **Done-criteria:** N/A — this is a standing constraint, not a task with an
  end state. Reassess only if CI itself needs to change (e.g., adding a
  Postgres service container once Agent 3 is triggered).

---

Cross-reference: the full SWOT this plan is derived from is available in the
session history that produced it; `ROADMAP.md` remains the source of truth
for version-level scope, `PROJECT_CHARTER.md` for the project's success
criteria and principles.
