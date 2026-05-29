from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DriftReport:
    source_table: str
    target_table: str
    missing_columns: list[str] = field(default_factory=list)
    extra_columns: list[str] = field(default_factory=list)
    type_mismatches: list[str] = field(default_factory=list)

    @property
    def is_clean(self) -> bool:
        return not (self.missing_columns or self.extra_columns or self.type_mismatches)

    @property
    def severity(self) -> str:
        if self.missing_columns:
            return "HIGH"
        if self.type_mismatches:
            return "MEDIUM"
        if self.extra_columns:
            return "LOW"
        return "NONE"

    def summary(self) -> str:
        if self.is_clean:
            return f"PASS: {self.source_table} matches {self.target_table}"
        return (
            f"FAIL: schema drift detected between {self.source_table} and {self.target_table} "
            f"(severity={self.severity})"
        )

    def render_detailed(self) -> str:
        lines = [
            "Drift details:",
            f"  missing_columns: {', '.join(self.missing_columns) if self.missing_columns else '[]'}",
            f"  extra_columns: {', '.join(self.extra_columns) if self.extra_columns else '[]'}",
            f"  type_mismatches: {', '.join(self.type_mismatches) if self.type_mismatches else '[]'}",
        ]
        return "\n".join(lines)
