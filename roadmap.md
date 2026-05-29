# Roadmap

## Current Progress
- Core schema comparison is implemented and tested.
- CSV extraction uses pandas with simple type inference.
- DuckDB schema extraction uses `PRAGMA table_info(...)`.
- CLI `schema-guard check` prints a drift report and returns the correct exit code.

## Next Steps
- Keep adding focused tests for edge cases and regression coverage.
- Refine report formatting only if user-facing clarity needs improvement.
