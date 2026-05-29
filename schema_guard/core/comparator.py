from __future__ import annotations

from collections.abc import Mapping
from typing import Any, cast

from schema_guard.core.normalizer import SchemaNormalizer
from schema_guard.models.schema import DriftComparison, NormalizedSchema, TableSchema

SchemaInput = TableSchema | NormalizedSchema | Mapping[str, Any]


def normalize_schema(schema: SchemaInput) -> NormalizedSchema:
    """Return a deterministic, comparable schema representation."""
    table_schema = _as_table_schema(schema)
    normalized = SchemaNormalizer().normalize(table_schema)
    return {"table": normalized.table, "columns": normalized.columns}


def compare_schemas(source: SchemaInput, target: SchemaInput) -> DriftComparison:
    """Compare two schemas and return a structured drift report."""
    normalized_source = normalize_schema(source)
    normalized_target = normalize_schema(target)

    source_columns = normalized_source["columns"]
    target_columns = normalized_target["columns"]

    source_names = set(source_columns)
    target_names = set(target_columns)

    missing_columns = sorted(target_names - source_names)
    extra_columns = sorted(source_names - target_names)
    type_mismatches = sorted(
        column_name
        for column_name in source_names & target_names
        if source_columns[column_name] != target_columns[column_name]
    )

    severity = classify_severity(
        missing_columns=missing_columns,
        type_mismatches=type_mismatches,
        extra_columns=extra_columns,
    )

    return {
        "source_table": normalized_source["table"],
        "target_table": normalized_target["table"],
        "missing_columns": missing_columns,
        "extra_columns": extra_columns,
        "type_mismatches": type_mismatches,
        "severity": severity,
        "is_clean": not (missing_columns or extra_columns or type_mismatches),
    }


def classify_severity(
    *,
    missing_columns: list[str],
    type_mismatches: list[str],
    extra_columns: list[str],
) -> str:
    if missing_columns:
        return "HIGH"
    if type_mismatches:
        return "MEDIUM"
    if extra_columns:
        return "LOW"
    return "NONE"


def _as_table_schema(schema: SchemaInput) -> TableSchema:
    if isinstance(schema, TableSchema):
        return schema

    table_name = str(schema.get("table", "")).strip()
    columns = schema.get("columns", {})
    if not isinstance(columns, Mapping):
        columns = {}

    normalized_columns = {
        str(column_name): str(column_type)
        for column_name, column_type in cast(Mapping[str, Any], columns).items()
    }
    return TableSchema(table=table_name, columns=normalized_columns)
