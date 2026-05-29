from __future__ import annotations

from pathlib import Path

import pandas as pd

from schema_guard.models.schema import TableSchema
from schema_guard.utils.type_inference import infer_series_type


class CSVSchemaExtractor:
    def extract(self, source_path: Path) -> TableSchema:
        dataframe = pd.read_csv(source_path)
        columns = {
            column_name.strip().lower(): infer_series_type(dataframe[column_name])
            for column_name in dataframe.columns
        }
        ordered_columns = dict(sorted(columns.items()))
        return TableSchema(table=source_path.stem.lower(), columns=ordered_columns)
