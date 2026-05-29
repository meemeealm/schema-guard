from __future__ import annotations

from pathlib import Path

import typer

from schema_guard.core.service import check_schema_drift
from schema_guard.models.drift import DriftReport

app = typer.Typer(add_completion=False, help="Detect schema drift before ingestion.")


@app.callback()
def cli() -> None:
    """Schema Guard command group."""


@app.command()
def check(
    # temp change ... to None to make optional 
    source: Path = typer.Option(..., exists=True, dir_okay=False, readable=True, help="CSV source file."),
    duckdb: Path = typer.Option(..., exists=True, dir_okay=False, readable=True, help="DuckDB database file."),
    table: str = typer.Option(..., help="Target DuckDB table."),
) -> None:
    """Check a CSV file against a DuckDB table."""
    report = check_schema_drift(source=source, duckdb_path=duckdb, table=table)

    typer.echo(format_report(report))
    raise typer.Exit(code=0 if report.is_clean else 1)


def format_report(report: DriftReport) -> str:
    lines = [
        report.summary(),
        "",
        f"Source table: {report.source_table}",
        f"Target table: {report.target_table}",
        f"Severity: {report.severity}",
        f"Missing columns in {report.target_table} table: {format_list(report.missing_columns)}",
        f"Extra columns: {format_list(report.extra_columns)}",
        f"Type mismatches: {format_list(report.type_mismatches)}",
    ]
    return "\n".join(lines)


def format_list(items: list[str]) -> str:
    return ", ".join(items) if items else "none"


def main() -> None:
    app()


if __name__ == "__main__":
    main()
