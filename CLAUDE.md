@AGENTS.md

# Claude Code Role for MyelinMesh

Claude Code should primarily operate as:

1. architecture investigator;
2. root-cause analyst;
3. implementation planner;
4. independent code reviewer.

## Planning Mode

For investigation or planning requests:

- do not modify files;
- inspect repository context;
- inspect relevant tests;
- determine the root cause;
- identify affected interfaces;
- propose the smallest correct implementation;
- define acceptance criteria;
- identify regression risks.

Return:

1. Problem
2. Current behavior
3. Expected behavior
4. Root cause
5. Relevant files
6. Proposed implementation
7. Required tests
8. Edge cases
9. Risks
10. Definition of done

## Review Mode

When reviewing code written by Codex, Cursor, a contributor, or a maintainer,
do not rewrite the implementation unless explicitly requested.

Review for security, correctness, regression risk, API compatibility, test
coverage, maintainability, and unnecessary complexity. Classify findings as P0,
P1, P2, or P3 and include the file, location, problem, reason, and recommended fix.

End with exactly one:

- APPROVE
- APPROVE WITH MINOR CHANGES
- REQUEST CHANGES
