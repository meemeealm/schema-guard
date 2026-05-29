from __future__ import annotations

from collections.abc import Iterable

import pandas as pd


def infer_series_type(values: pd.Series) -> str:
    """Infer a simple schema type from a pandas series."""
    non_null_values = [value for value in values.dropna().tolist() if str(value).strip()]
    if not non_null_values:
        return "string"

    if all(_is_bool(value) for value in non_null_values):
        return "bool"
    if all(_is_int(value) for value in non_null_values):
        return "int"
    if all(_is_numeric(value) for value in non_null_values):
        return "float"
    return "string"


def infer_type_from_values(values: Iterable[object]) -> str:
    """Infer a simple schema type from raw values."""
    series = pd.Series(list(values))
    return infer_series_type(series)


def _is_bool(value: object) -> bool:
    normalized = str(value).strip().lower()
    return normalized in {"true", "false"}


def _is_int(value: object) -> bool:
    normalized = str(value).strip()
    if not normalized:
        return False
    try:
        int(normalized)
    except ValueError:
        return False
    return True


def _is_numeric(value: object) -> bool:
    normalized = str(value).strip()
    if not normalized:
        return False
    try:
        float(normalized)
    except ValueError:
        return False
    return True
