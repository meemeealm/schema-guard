from __future__ import annotations

import unittest

from schema_guard.core.normalizer import normalize_schema
from schema_guard.models.schema import TableSchema


class SchemaNormalizerTests(unittest.TestCase):
    def test_normalizes_names_and_types_deterministically(self) -> None:
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

        self.assertEqual(normalized.table, "authors")
        self.assertEqual(
            normalized.columns,
            {
                "alias": "string",
                "id": "int",
                "meta": "string",
                "name": "string",
                "score": "int",
            },
        )


if __name__ == "__main__":
    unittest.main()
