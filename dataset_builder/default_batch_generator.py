from datetime import datetime, timedelta
import pandas as pd
from uuid import uuid4
from typing import Generator

from dataset_builder.batch_generator_interface import BatchGenerator
from interaction_templates.core.base_event_context import BaseEventContext
from interaction_templates.interaction_builder import generate_interaction
from interaction_templates.anomalies.injector import AnomalyInjector

class DefaultBatchGenerator(BatchGenerator):
    def __init__(self, cxm: str, apply_anomalies: bool = False, anomaly_config_path: str = None):
        self.cxm = cxm
        self.apply_anomalies = apply_anomalies
        self.anomaly_config_path = anomaly_config_path
        self.injector = AnomalyInjector(anomaly_config_path, cxm) if apply_anomalies else None
        self.generated_events = []
        self.anomaly_metrics = {}

    def generate(self, schema: list[dict], base_timestamp: datetime, interaction_spacing_seconds: int = 15) -> pd.DataFrame:
        current_time = base_timestamp

        for block in schema:
            channel = block["channel"]
            interaction_type = block["interaction_type"]
            count = block["count"]

            for _ in range(count):
                interaction_id = str(uuid4())

                context = BaseEventContext(
                    interaction_id=interaction_id,
                    timestamp=current_time.isoformat(),
                    channel=channel,
                    event_type="placeholder"
                )

                events = generate_interaction(interaction_type, context)

                if self.injector:
                    events = self.injector.apply_to_interaction(events, interaction_type)
                    events = [self.injector.apply_to_event(e, e["event_type"]) for e in events]

                self.generated_events.extend(events)
                current_time += timedelta(seconds=interaction_spacing_seconds)

        df = pd.DataFrame(self.generated_events)

        if self.injector:
            self.anomaly_metrics = self.injector.get_metrics()

        return df

    def stream(self, schema: list[dict], base_timestamp: datetime, interaction_spacing_seconds: int = 15) -> Generator[dict, None, None]:
        current_time = base_timestamp

        for block in schema:
            channel = block["channel"]
            interaction_type = block["interaction_type"]
            count = block["count"]

            for _ in range(count):
                interaction_id = str(uuid4())

                context = BaseEventContext(
                    interaction_id=interaction_id,
                    timestamp=current_time.isoformat(),
                    channel=channel,
                    event_type="placeholder"
                )

                events = generate_interaction(interaction_type, context)

                if self.injector:
                    events = self.injector.apply_to_interaction(events, interaction_type)
                    events = [self.injector.apply_to_event(e, e["event_type"]) for e in events]

                for event in events:
                    yield event

                current_time += timedelta(seconds=interaction_spacing_seconds)

    def export(self, path: str, format: str = "csv"):
        df = pd.DataFrame(self.generated_events)

        if format == "csv":
            df.to_csv(path, index=False)
        elif format == "json":
            df.to_json(path, orient="records", lines=True)
        elif format == "parquet":
            df.to_parquet(path, index=False)
        else:
            raise ValueError(f"Unsupported export format: {format}")

    def get_anomaly_metrics(self) -> dict:
        return self.anomaly_metrics
