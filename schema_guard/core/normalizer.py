from __future__ import annotations

from collections.abc import Mapping

from schema_guard.models.schema import TableSchema
from schema_guard.utils.normalization import normalize_type_name


def normalize_column_name(column_name: str) -> str:
    return column_name.strip().lower()


def normalize_table_name(table_name: str) -> str:
    return table_name.strip().lower()


def normalize_columns(columns: Mapping[str, str]) -> dict[str, str]:
    normalized_columns = {
        normalize_column_name(column_name): normalize_type_name(column_type)
        for column_name, column_type in columns.items()
    }
    return dict(sorted(normalized_columns.items()))


def normalize_schema(schema: TableSchema) -> TableSchema:
    return TableSchema(
        table=normalize_table_name(schema.table),
        columns=normalize_columns(schema.columns),
    )


class SchemaNormalizer:
    def normalize(self, schema: TableSchema) -> TableSchema:
        return normalize_schema(schema)
