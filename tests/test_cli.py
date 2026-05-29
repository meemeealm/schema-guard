from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import duckdb
from typer.testing import CliRunner

from schema_guard.cli import app


class CliTests(unittest.TestCase):
    def test_check_command_returns_zero_for_matching_schema(self) -> None:
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as temporary_directory:
            temp_dir = Path(temporary_directory)
            csv_path = temp_dir / "authors.csv"
            db_path = temp_dir / "example.duckdb"

            csv_path.write_text("id,name\n1,Ada\n", encoding="utf-8")

            connection = duckdb.connect(str(db_path))
            try:
                connection.execute("create table authors(id integer, name varchar)")
            finally:
                connection.close()

            result = runner.invoke(
                app,
                [
                    "check",
                    "--source",
                    str(csv_path),
                    "--duckdb",
                    str(db_path),
                    "--table",
                    "authors",
                ],
            )

            self.assertEqual(result.exit_code, 0, msg=result.output)
            self.assertIn("PASS:", result.output)
            self.assertIn("Severity: NONE", result.output)
            self.assertIn("Missing columns: none", result.output)

    def test_check_command_returns_one_for_drift(self) -> None:
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as temporary_directory:
            temp_dir = Path(temporary_directory)
            csv_path = temp_dir / "authors.csv"
            db_path = temp_dir / "example.duckdb"

            csv_path.write_text("id,name\n1,Ada\n", encoding="utf-8")

            connection = duckdb.connect(str(db_path))
            try:
                connection.execute("create table authors(id integer)")
            finally:
                connection.close()

            result = runner.invoke(
                app,
                [
                    "check",
                    "--source",
                    str(csv_path),
                    "--duckdb",
                    str(db_path),
                    "--table",
                    "authors",
                ],
            )

            self.assertEqual(result.exit_code, 1, msg=result.output)
            self.assertIn("FAIL:", result.output)
            self.assertIn("Severity: LOW", result.output)
            self.assertIn("Extra columns: name", result.output)


if __name__ == "__main__":
    unittest.main()
