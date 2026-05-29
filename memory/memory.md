# Schema Guard Memory

## Architectural Decisions
- Project name: `schema-guard`
- Runtime: Python `3.10+`
- Environment/tooling: `uv`
- CLI framework: `Typer`
- DuckDB integration: `duckdb` Python package with `PRAGMA table_info(...)`
- Packaging: `pyproject.toml` with a console script entry point `schema-guard = schema_guard.cli:main`
- Package layout:
  - `schema_guard/core/` for pure business logic
  - `schema_guard/connectors/` for system integrations
  - `schema_guard/models/` for schema and drift types
  - `schema_guard/utils/` for helper functions
  - `schema_guard/cli.py` for CLI only

## Canonical Schema Format
- All schema objects use:
  - `{"table": "...", "columns": {"column_name": "type"}}`
- Column names are normalized to lowercase and trimmed.
- Schema comparison is set-based and deterministic.
- Column order does not affect drift detection.

## Drift Classification
- `HIGH`: missing columns / breaking changes
- `MEDIUM`: type mismatches
- `LOW`: extra columns in target

## Workflow
1. Extract source schema from CSV.
2. Extract target schema from DuckDB.
3. Normalize both schemas.
4. Compare schemas in core logic.
5. Produce a structured drift report.
6. CLI prints summary first, then detailed diff.
7. Exit code `0` for no drift, `1` for drift detected.

## Implementation Rules
- Keep comparison logic pure and unit-testable.
- Do not print inside core modules.
- Do not mix CLI logic with business logic.
- Do not embed SQL in comparator logic.
- Reuse connectors instead of bypassing them.

## Current Status
- CSV extraction uses pandas.
- DuckDB schema extraction uses `PRAGMA table_info(...)`.
- Comparison returns structured dict output.
- Tests exist for extractor, connector, comparator, and CLI.
- CLI `schema-guard check` is implemented with human-readable output and exit codes.
- Schema normalization is implemented with deterministic table/column canonicalization.
- `memory/memory.md` should be read before making further changes.
- `memory/roadmap.md` is the active short progress log for implementation work.
