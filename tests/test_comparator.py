from __future__ import annotations

from schema_guard.core.comparator import compare_schemas
from schema_guard.models.schema import TableSchema


def test_detects_missing_columns() -> None:
    source = TableSchema(table="source", columns={"id": "int"})
    target = TableSchema(table="target", columns={"id": "int", "name": "string"})

    comparison = compare_schemas(source, target)

    assert comparison["is_clean"] is False
    assert comparison["missing_columns"] == ["name"]
    assert comparison["extra_columns"] == []
    assert comparison["type_mismatches"] == []
    assert comparison["severity"] == "HIGH"


def test_detects_type_mismatches() -> None:
    source = TableSchema(table="source", columns={"id": "int", "name": "string"})
    target = TableSchema(table="target", columns={"id": "string", "name": "string"})

    comparison = compare_schemas(source, target)

    assert comparison["is_clean"] is False
    assert comparison["missing_columns"] == []
    assert comparison["extra_columns"] == []
    assert comparison["type_mismatches"] == ["id"]
    assert comparison["severity"] == "MEDIUM"
