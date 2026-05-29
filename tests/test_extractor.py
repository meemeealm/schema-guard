from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from schema_guard.core.extractor import CSVSchemaExtractor


class CSVSchemaExtractorTests(unittest.TestCase):
    def test_extracts_headers(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            csv_path = Path(temporary_directory) / "authors.csv"
            csv_path.write_text("id,name\n1,Ada\n", encoding="utf-8")

            schema = CSVSchemaExtractor().extract(csv_path)

            self.assertEqual(schema.table, "authors")
            self.assertEqual(schema.columns, {"id": "int", "name": "string"})

    def test_infers_bool_float_and_string(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            csv_path = Path(temporary_directory) / "mixed.csv"
            csv_path.write_text("flag,score,notes\ntrue,1.5,hello\nfalse,2.0,world\n", encoding="utf-8")

            schema = CSVSchemaExtractor().extract(csv_path)

            self.assertEqual(schema.columns, {"flag": "bool", "notes": "string", "score": "float"})


if __name__ == "__main__":
    unittest.main()
