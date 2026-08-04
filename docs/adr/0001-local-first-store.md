# ADR 0001: Use a local-first JSON and SQLite store

- Status: Accepted
- Date: 2026-08-04

## Context

The project needs a transparent starting point that works for researchers and contributors without infrastructure setup.

## Decision

Store normalized records as individual JSON files and maintain searchable metadata in SQLite.

## Consequences

Advantages:

- Easy inspection and versioning
- No external service
- Simple backup and export
- Clear separation between records and large artifacts

Limitations:

- Limited concurrent writes
- Basic search only
- No built-in vector retrieval
- Future migrations needed for large deployments
