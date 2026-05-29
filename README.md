# Schema Guard

`schema-guard` detects schema drift between CSV sources and DuckDB tables before ingestion.

## Install

```bash
uv sync
```

## Check a schema

```bash
schema-guard check --source data.csv --duckdb warehouse.duckdb --table authors
```
