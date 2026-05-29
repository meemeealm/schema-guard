from __future__ import annotations

from schema_guard.models.drift import DriftReport


class DriftReporter:
    def render(self, report: DriftReport) -> str:
        return report.render_detailed()
