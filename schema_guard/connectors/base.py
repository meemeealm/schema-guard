from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import Any

from schema_guard.models.schema import NormalizedSchema


class BaseConnector(ABC):
    @abstractmethod
    def get_schema(self, table: str) -> NormalizedSchema | Mapping[str, Any]:
        raise NotImplementedError
