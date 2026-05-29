from __future__ import annotations

from pathlib import Path

from schema_guard.connectors.duckdb import DuckDBConnector
from schema_guard.core.comparator import compare_schemas
from schema_guard.core.extractor import CSVSchemaExtractor
from schema_guard.models.drift import DriftReport


def check_schema_drift(source: Path, duckdb_path: Path, table: str) -> DriftReport:
    extractor = CSVSchemaExtractor()
    connector = DuckDBConnector(duckdb_path)

    source_schema = extractor.extract(source)
    target_schema = connector.get_schema(table)
    comparison = compare_schemas(source_schema, target_schema)
    return DriftReport(
        source_table=comparison["source_table"],
        target_table=comparison["target_table"],
        missing_columns=comparison["missing_columns"],
        extra_columns=comparison["extra_columns"],
        type_mismatches=comparison["type_mismatches"],
    )
