from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import duckdb

from schema_guard.connectors.duckdb import DuckDBConnector, extract_schema


class DuckDBConnectorTests(unittest.TestCase):
    def test_reads_table_schema(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "example.duckdb"
            connection = duckdb.connect(str(database_path))
            try:
                connection.execute("create table authors(id integer, name varchar)")
            finally:
                connection.close()

            schema = DuckDBConnector(database_path).get_schema("authors")

            self.assertEqual(schema, {"table": "authors", "columns": {"id": "INTEGER", "name": "VARCHAR"}})

    def test_extract_schema_function_returns_canonical_dict(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "example.duckdb"
            connection = duckdb.connect(str(database_path))
            try:
                connection.execute("create table authors(id integer, name varchar)")
            finally:
                connection.close()

            schema = extract_schema(database_path, "authors")

            self.assertEqual(schema["table"], "authors")
            self.assertEqual(schema["columns"], {"id": "INTEGER", "name": "VARCHAR"})


if __name__ == "__main__":
    unittest.main()
