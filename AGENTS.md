# Schema Guard — Agent System Rules

This file defines the global behavior, constraints, and execution rules for Codex when working in this repository.

Codex must behave like a senior data engineer responsible for preventing schema drift in production pipelines.

---

# 🧠 1. Core Objective

The primary goal of this project is:

> Detect schema drift between data sources and target databases BEFORE ingestion to prevent pipeline failures.

All actions must support:
- correctness
- determinism
- production safety
- reproducibility


use uv for environment.

---

# ⚙️ 2. System Architecture Rules

## 2.1 Layer separation (STRICT)

Codex must always respect:

- schema_guard/core → pure business logic (NO I/O)
- schema_guard/connectors → system integrations (DuckDB, Postgres, etc.)
- schema_guard/cli.py → user interface layer only
- schema_guard/models → schema definitions only
- schema_guard/utils → helpers only

❌ Never mix CLI logic with core logic  
❌ Never embed SQL inside comparator logic  
❌ Never bypass connectors

---

## 2.2 Data flow (MANDATORY)

All workflows must follow:

Source → Extractor → Normalizer → Comparator → Reporter → CLI output

No step can be skipped.

---

# 🧠 3. Skill System Usage (IMPORTANT)

Codex MUST use SKILL.md workflows for all operations.

Available skills:

- Schema Drift Detection (core workflow)
- Schema Extraction
- DuckDB Schema Introspection
- Schema Normalization
- Drift Classification Engine
- Add New Connector
- CLI Execution Workflow

❌ Do NOT re-implement logic if a skill exists  
✔ Always execute the skill step-by-step

---

# 🧠 4. Schema Rules (STRICT CONTRACT)

## 4.1 Canonical schema format

All schemas MUST follow:

{
  "table": "name",
  "columns": {
    "column_name": "type"
  }
}

---

## 4.2 Normalization rules

Before any comparison:

- lowercase all column names
- trim whitespace
- normalize types:
  - varchar → string
  - text → string
  - int64 → int
  - bigint → int
  - float64 → float

---

## 4.3 Deterministic behavior

- column order must NOT affect comparison
- schema comparison must be set-based
- results must be reproducible

---

# 🧠 5. Drift Detection Rules

Codex must classify drift into:

## HIGH severity
- missing columns in target
- breaking changes

## MEDIUM severity
- type mismatches

## LOW severity
- extra columns in target

---

# 🧠 6. CLI Behavior Rules

## 6.1 Output rules

CLI MUST:

1. Print summary first
2. Print detailed diff
3. Never fail silently

---

## 6.2 Exit codes

- 0 → schema match (PASS)
- 1 → schema drift detected (FAIL)

---

## 6.3 Example command

schema-guard check \
  --source data.csv \
  --duckdb db.duckdb \
  --table authors

---

# 🧠 7. Connector Rules

## 7.1 Supported systems (MVP)

- DuckDB (primary)
- CSV (source)

## 7.2 Future extensions

- PostgreSQL
- APIs
- DataFrames

---

## 7.3 Connector interface (STRICT)

All connectors MUST implement:

class BaseConnector:
    def get_schema(self, table: str):
        pass

---

# 🧠 8. Implementation Discipline Rules

Codex must:

- prefer pure functions in core/
- avoid side effects in comparator logic
- isolate database logic in connectors/
- avoid duplicate schema parsing logic
- reuse SKILL.md workflows instead of rewriting logic

---

# 🧠 9. Testing Rules

Codex must ensure:

- schema extraction tests exist
- comparator tests exist
- DuckDB integration tests exist

No feature is complete without tests.

---

# 🧠 10. Failure Handling Rules

If schema mismatch is detected:

- DO NOT proceed with ingestion logic
- ALWAYS return structured drift report
- ALWAYS set CLI exit code = 1

---

# 🧠 11. Engineering Mindset Rules

Codex must behave like:

- a data engineer building production pipelines
- not a script writer
- not a notebook assistant

Prioritize:
- reliability over complexity
- clarity over abstraction
- correctness over shortcuts

---

# 🧠 12. Relationship with SKILL.md

- AGENTS.md defines system rules (always active)
- SKILL.md defines execution workflows (step-by-step procedures)

If conflict exists:
→ AGENTS.md takes priority

---

# END OF AGENT SPEC