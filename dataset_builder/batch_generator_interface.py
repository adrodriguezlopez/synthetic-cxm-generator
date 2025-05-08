from abc import ABC, abstractmethod
from typing import Generator
import pandas as pd
from datetime import datetime

class BatchGenerator(ABC):
    """
    Base interface for batch or streaming interaction generators.
    """

    @abstractmethod
    def generate(self, schema: list[dict], base_timestamp: datetime, interaction_spacing_seconds: int = 15) -> pd.DataFrame:
        """Generates all interactions as defined in the schema and returns a DataFrame."""
        pass

    @abstractmethod
    def stream(self, schema: list[dict], base_timestamp: datetime, interaction_spacing_seconds: int = 15) -> Generator[dict, None, None]:
        """Generates events one-by-one progressively (streaming mode)."""
        pass

    @abstractmethod
    def export(self, path: str, format: str = "csv"):
        """Exports generated events to a file in the specified format."""
        pass

    @abstractmethod
    def get_anomaly_metrics(self) -> dict:
        """Returns a summary of applied anomalies."""
        pass
