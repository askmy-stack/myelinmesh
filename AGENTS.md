# MyelinMesh Engineering Instructions

## Project Mission

MyelinMesh is an open-source reliability evidence mesh for AI systems.

The project connects evidence about:

- system changes
- tests
- traces
- failures
- diagnoses
- recovery actions
- provenance

Engineering work should reinforce reliability, observability, traceability,
reproducibility, interoperability, and safe recovery of AI systems.

## Engineering Philosophy

- Prefer small, reviewable changes.
- One issue per branch.
- Solve the smallest complete problem.
- Avoid unrelated refactors.
- Do not add abstractions without a concrete present need.
- Preserve backward compatibility unless the task explicitly changes it.
- Inspect existing implementation before introducing new patterns.
- Prefer consistency with the repository over introducing a new personal style.
- Never optimize for commit count.

## Before Coding

Before modifying implementation files:

1. Read the relevant issue or task completely.
2. Inspect the affected source code.
3. Inspect related tests.
4. Inspect nearby abstractions and call sites.
5. Review recent relevant changes when useful.
6. Reproduce bugs before fixing them when reasonably possible.
7. Define acceptance criteria.
8. Identify the smallest correct implementation.

If requirements are materially ambiguous, stop implementation and report the ambiguity.

## Python

Follow `pyproject.toml` as the source of truth for supported Python versions,
linting, formatting, typing, tests, package structure, and dependencies.

Do not silently weaken repository quality checks.

## Validation

For meaningful Python changes, run the checks configured by the repository.

Expected validation includes, where applicable:

```bash
python -m pytest
ruff check .
ruff format --check .
mypy -p myelinmesh
pre-commit run --all-files
```

If the exact commands differ from repository configuration, use the repository-defined equivalents.

Never claim a check passed unless it was actually executed successfully.

If a check cannot run because of the environment:

1. report the exact command;
2. report the failure;
3. explain why it could not be validated.

## Bug Fixes

For bug fixes:

1. reproduce or characterize the failure;
2. add a regression test when practical;
3. implement the smallest fix;
4. verify the regression test;
5. run relevant broader tests.

Do not merely suppress the symptom.

## Features

For new functionality:

- define acceptance criteria;
- preserve existing APIs unless intentionally changing them;
- add positive tests;
- add negative or edge-case tests where appropriate;
- document externally visible behavior;
- avoid expanding scope beyond the issue.

## Dependencies

Do not add a production dependency unless necessary.

Before introducing one:

- explain why the standard library is insufficient;
- explain why existing dependencies are insufficient;
- assess maintenance impact;
- assess security implications;
- confirm license compatibility when relevant.

Never introduce a dependency merely to simplify a trivial implementation.

## Security

Never:

- commit credentials;
- expose secrets;
- log authentication tokens;
- disable security validation to make tests pass;
- trust external input without appropriate validation;
- silently broaden permissions.

Treat files, network input, tool responses, model output, and external metadata as untrusted where appropriate.

## Git Workflow

Never commit directly to `main`.

Use branch names such as:

```text
feat/<issue>-short-description
fix/<issue>-short-description
test/<issue>-short-description
docs/<issue>-short-description
chore/<short-description>
agent/<short-description>
oss/<issue>-short-description
```

Prefer one issue or coherent engineering objective per branch.

Do not merge automatically.

Do not force-push unless explicitly authorized by the maintainer.

## Commit Quality

Commits should represent meaningful engineering units.

Avoid:

- empty commits;
- artificial commit splitting;
- formatting-only churn mixed into feature commits;
- automated edits unrelated to the task;
- commits created only to increase contribution activity.

## Pull Requests

Every meaningful PR should explain:

### Problem

What is wrong, missing, or being improved?

### Root Cause / Context

Why does the problem exist?

### Solution

What changed and why was this approach selected?

### Testing

Which commands were executed and what were the results?

### Risks

What could regress or require follow-up?

### Scope

Confirm whether unrelated changes were avoided.

Where appropriate, link the issue using:

```text
Closes #<issue>
```

## Code Review Severity

Use:

- **P0** — security vulnerability, data loss/corruption, catastrophic correctness problem
- **P1** — likely regression, broken behavior, API incompatibility, major missing test
- **P2** — maintainability, performance, design weakness, unnecessary complexity
- **P3** — non-blocking style, documentation, or optional improvement

Do not request changes solely for subjective preference.

## AI Agent Responsibilities

AI agents may inspect, investigate, reproduce, plan, implement, test, review,
draft documentation, and draft PR descriptions.

AI agents must not:

- merge their own PRs;
- invent requirements;
- fabricate test results;
- hide failed validation;
- modify unrelated code;
- introduce dependencies silently;
- disable tests to obtain green CI;
- commit secrets;
- push directly to protected/default branches;
- create artificial activity for contribution statistics.

## Multi-Agent Rule

For meaningful implementation work:

> One issue → one implementation agent → one isolated branch/worktree.

A different agent should review the implementation when practical.

Example:

```text
Claude Code → investigate / plan
Codex       → implement / test
Claude Code → independent review
Cursor      → maintainer inspection / targeted fixes
Human       → approve / merge
```

Do not have multiple coding agents concurrently modify the same branch.

## Human Maintainer Gate

A human maintainer owns prioritization, architectural approval, acceptance of
behavioral changes, interpretation of ambiguous requirements, final PR approval,
and merge decisions.

Before merge, the maintainer should be able to explain:

1. What problem does this solve?
2. Why did the problem happen?
3. Why does this implementation solve it?
4. What could regress?
5. How was the change validated?

## Definition of Done

Work is not complete until:

- requested behavior is implemented;
- scope is controlled;
- relevant tests pass;
- lint/format/type checks pass when applicable;
- no secrets are present;
- no unexplained dependency changes exist;
- documentation is updated when needed;
- the diff has been reviewed;
- remaining risks are explicitly reported.
