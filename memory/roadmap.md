# Roadmap

## Current Progress
- Core schema comparison is implemented and tested.
- CSV extraction uses pandas with simple type inference.
- DuckDB schema extraction uses `PRAGMA table_info(...)`.
- CLI `schema-guard check` prints a drift report and returns the correct exit code.
- Schema normalization now canonicalizes names and type aliases deterministically.
- Comparator and normalizer tests now use `pytest` and cover missing columns, type mismatches, and normalization.
- README has been expanded with structure, workflow, and architecture notes.

## Next Steps
- Keep adding focused tests for edge cases and regression coverage.
- Refine report formatting only if user-facing clarity needs improvement.
