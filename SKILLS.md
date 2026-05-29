# Schema Guard Skills

This file defines reusable workflows for Codex to execute schema validation, drift detection, and connector extension tasks.

Each skill is a structured procedure. Follow steps strictly unless explicitly overridden.

---

# Skill 1: Schema Drift Detection (Core Workflow)

## Purpose
Detect differences between source and target schemas before ingestion.

## When to use
- CSV → DuckDB validation
- DataFrame → DB validation
- Pre-ingestion checks

## Inputs
- source (CSV / DataFrame / JSON)
- target (DuckDB table / schema object)

## Steps

1. Extract source schema
   - If CSV: read headers + infer types
   - If DataFrame: use dtypes

2. Extract target schema
   - Query DuckDB using:
     PRAGMA table_info(table_name)

3. Normalize both schemas
   - lowercase column names
   - map types:
     int64 → int
     float64 → float
     object → string

4. Compare schemas
   - missing_columns = target - source
   - extra_columns = source - target
   - type_mismatches = shared columns with different types

5. Generate drift report
   - categorize severity:
     - missing column → HIGH
     - type mismatch → MEDIUM
     - extra column → LOW

6. Return structured output:
   - status: PASS / FAIL
   - diff summary
   - human-readable report

---

# Skill 2: Schema Extraction (Source Systems)

## Purpose
Standardize schema extraction from raw inputs.

## Supported sources
- CSV files
- pandas DataFrame
- JSON records

## Steps

1. Detect input type
2. Extract columns
3. Infer types:
   - int
   - float
   - string
   - boolean
4. Return canonical schema format:

{
  "table": "source",
  "columns": {
    "col1": "type",
    "col2": "type"
  }
}

---

# Skill 3: DuckDB Schema Introspection

## Purpose
Extract schema from DuckDB tables.

## Steps

1. Connect to DuckDB database
2. Run query:

   PRAGMA table_info(table_name);

3. Extract:
   - column name
   - data type
4. Normalize types
5. Return canonical schema format

---

# Skill 4: Schema Normalization

## Purpose
Ensure all schemas are comparable.

## Rules

- Convert all column names to lowercase
- Remove whitespace
- Normalize types:
  - varchar → string
  - text → string
  - bigint → int
- Sort columns alphabetically

## Output

Always return deterministic schema format:
{
  "columns": { ... }
}

---

# Skill 5: Drift Classification Engine

## Purpose
Classify schema differences into meaningful categories.

## Rules

- Missing column in target → HIGH severity
- Extra column in target → LOW severity
- Type mismatch → MEDIUM severity

## Output format

{
  "missing": [],
  "extra": [],
  "type_mismatch": [],
  "severity": "LOW | MEDIUM | HIGH"
}

---

# 🧠 Skill 6: Add New Connector (Extensibility Skill)

## Purpose
Add support for new data systems (e.g. PostgreSQL).

## Steps

1. Create new file in connectors/
   - postgres.py

2. Implement interface:

   class BaseConnector:
       def get_schema(self, table): pass

3. Implement schema extraction using system metadata:
   - Postgres: information_schema.columns

4. Return canonical schema format

5. Register connector in core system

---

# 🧠 Skill 7: CLI Execution Workflow

## Purpose
Ensure CLI behaves consistently.

## Steps

1. Parse CLI arguments
2. Call appropriate connector(s)
3. Run schema drift detection
4. Print human-readable report
5. Set exit code:
   - 0 → no drift
   - 1 → drift detected

## Output rules

- Always print summary first
- Then detailed diff
- Never fail silently