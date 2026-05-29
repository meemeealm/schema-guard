from __future__ import annotations

from schema_guard.core.normalizer import normalize_schema
from schema_guard.models.schema import TableSchema


def test_normalizes_names_and_types_deterministically() -> None:
    schema = TableSchema(
        table=" Authors ",
        columns={
            "Name ": "TEXT",
            " ID": "BIGINT",
            "alias": "VARCHAR",
            "meta": "OBJECT",
            "score": "int64",
        },
    )

    normalized = normalize_schema(schema)

    assert normalized.table == "authors"
    assert normalized.columns == {
        "alias": "string",
        "id": "int",
        "meta": "string",
        "name": "string",
        "score": "int",
    }
