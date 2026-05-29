from __future__ import annotations

from pathlib import Path

import duckdb

from schema_guard.connectors.base import BaseConnector
from schema_guard.models.schema import NormalizedSchema


class DuckDBConnector(BaseConnector):
    def __init__(self, database_path: Path) -> None:
        self._database_path = Path(database_path)

    def get_schema(self, table: str) -> NormalizedSchema:
        return extract_schema(self._database_path, table)


def extract_schema(database_path: Path, table: str) -> NormalizedSchema:
    """Extract a DuckDB table schema in canonical dict format."""
    connection = duckdb.connect(str(database_path))
    try:
        safe_table = table.replace("'", "''")
        rows = connection.execute(f"PRAGMA table_info('{safe_table}')").fetchall()
    finally:
        connection.close()

    columns = {str(row[1]): str(row[2]) for row in rows}
    return {"table": table, "columns": columns}
