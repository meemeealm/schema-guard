from __future__ import annotations

import unittest

from schema_guard.core.comparator import compare_schemas, normalize_schema
from schema_guard.models.schema import TableSchema


class SchemaComparatorTests(unittest.TestCase):
    def test_detects_missing_columns(self) -> None:
        source = TableSchema(table="source", columns={"id": "int"})
        target = TableSchema(table="target", columns={"id": "int", "name": "string"})

        comparison = compare_schemas(source, target)

        self.assertFalse(comparison["is_clean"])
        self.assertEqual(comparison["missing_columns"], ["name"])
        self.assertEqual(comparison["extra_columns"], [])
        self.assertEqual(comparison["type_mismatches"], [])
        self.assertEqual(comparison["severity"], "HIGH")

    def test_normalizes_before_comparison(self) -> None:
        source = {"table": "Source", "columns": {"ID": "INT64", "Name": "TEXT"}}
        target = {"table": "target", "columns": {"name": "string", "id": "int"}}

        comparison = compare_schemas(source, target)

        self.assertTrue(comparison["is_clean"])
        self.assertEqual(comparison["severity"], "NONE")

        normalized = normalize_schema(source)
        self.assertEqual(normalized["table"], "source")
        self.assertEqual(normalized["columns"], {"id": "int", "name": "string"})


if __name__ == "__main__":
    unittest.main()
