import random
import yaml
import pandas as pd
from interaction_templates.anomalies.registry import get_anomaly_class

class AnomalyInjector:
    def __init__(self, config_path: str, cxm: str = "default"):
        self.cxm = cxm
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

    def apply_to_event(self, event: dict, event_type: str) -> dict:
        """
        Apply configured event-level anomalies to a single event.
        """
        anomalies = self.config.get(event_type, {}).get("anomalies", [])
        for anomaly_def in anomalies:
            if anomaly_def.get("category") != "event":
                continue
            if anomaly_def.get("cxm") and anomaly_def["cxm"] != self.cxm:
                continue

            anomaly_cls = get_anomaly_class(anomaly_def["type"], "event")
            fields = anomaly_def.get("fields", {})
            params = anomaly_def.get("params", {})

            if isinstance(fields, list):
                # Uniform config for all fields
                for field in fields:
                    if field in event and random.random() < anomaly_def.get("probability", 1.0):
                        anomaly = anomaly_cls(**params)
                        event[field] = anomaly.apply(event[field])
            elif isinstance(fields, dict):
                # Field-specific config
                for field, field_conf in fields.items():
                    if field in event:
                        probability = field_conf.get("probability", anomaly_def.get("probability", 1.0))
                        if random.random() < probability:
                            merged_params = {**params, **field_conf}
                            anomaly = anomaly_cls(**merged_params)
                            event[field] = anomaly.apply(event[field])

        return event

    def apply_to_interaction(self, events: list[dict], interaction_type: str) -> list[dict]:
        """
        Applies interaction-level anomalies to a full list of events representing one interaction.
        """
        if not events:
            return events

        anomalies = self.config.get(interaction_type, {}).get("anomalies", [])

        for anomaly_def in anomalies:
            if anomaly_def.get("category") != "interaction":
                continue
            if anomaly_def.get("cxm") and anomaly_def["cxm"] != self.cxm:
                continue

            probability = anomaly_def.get("probability", 1.0)
            if random.random() > probability:
                continue  # Skip this anomaly if it doesn't activate

            anomaly_cls = get_anomaly_class(anomaly_def["type"], "interaction")
            params = anomaly_def.get("params", {})
            anomaly = anomaly_cls(**params)

            # Apply the anomaly to the entire interaction
            events = anomaly.apply(events)

        return events

    def apply_to_dataset(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applies dataset-level anomalies to the full dataset (as a DataFrame).
        """
        if df.empty:
            return df

        anomalies = self.config.get("__dataset__", {}).get("anomalies", [])

        for anomaly_def in anomalies:
            if anomaly_def.get("category") != "dataset":
                continue
            if anomaly_def.get("cxm") and anomaly_def["cxm"] != self.cxm:
                continue

            probability = anomaly_def.get("probability", 1.0)
            if random.random() > probability:
                continue

            anomaly_cls = get_anomaly_class(anomaly_def["type"], "dataset")
            params = anomaly_def.get("params", {})
            anomaly = anomaly_cls(**params)

            df = anomaly.apply(df)

        return df