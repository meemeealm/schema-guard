from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypedDict


@dataclass(frozen=True)
class TableSchema:
    table: str
    columns: dict[str, str] = field(default_factory=dict)


class NormalizedSchema(TypedDict):
    table: str
    columns: dict[str, str]


class DriftComparison(TypedDict):
    source_table: str
    target_table: str
    missing_columns: list[str]
    extra_columns: list[str]
    type_mismatches: list[str]
    severity: str
    is_clean: bool
