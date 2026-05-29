from __future__ import annotations

TYPE_ALIASES = {
    "varchar": "string",
    "text": "string",
    "object": "string",
    "string": "string",
    "int64": "int",
    "bigint": "int",
    "integer": "int",
    "float64": "float",
    "double": "float",
    "boolean": "bool",
    "bool": "bool",
}


def normalize_type_name(type_name: str) -> str:
    return TYPE_ALIASES.get(type_name.strip().lower(), type_name.strip().lower())
