import random
import yaml
import pandas as pd
from collections import defaultdict
from interaction_templates.anomalies.registry import get_anomaly_class

class AnomalyInjector:
    def __init__(self, config_path: str, cxm: str = "default"):
        self.cxm = cxm
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
        self.anomaly_stats = defaultdict(int)

    def apply_to_event(self, event: dict, event_type: str) -> dict:
        anomalies = self.config.get(event_type, {}).get("anomalies", [])
        for anomaly_def in anomalies:
            if anomaly_def.get("category") != "event":
                continue
            if anomaly_def.get("cxm") and anomaly_def["cxm"] != self.cxm:
                continue

            anomaly_cls = get_anomaly_class(anomaly_def["type"], "event")
            fields = anomaly_def.get("fields", {})
            params = anomaly_def.get("params", {})
            anomaly_type = anomaly_def["type"]

            if isinstance(fields, list):
                for field in fields:
                    if field in event and random.random() < anomaly_def.get("probability", 1.0):
                        anomaly = anomaly_cls(**params)
                        event[field] = anomaly.apply(event[field])
                        self.anomaly_stats[anomaly_type] += 1
                        event.setdefault("anomalies_applied", []).append(anomaly_type)

            elif isinstance(fields, dict):
                for field, field_conf in fields.items():
                    if field in event:
                        probability = field_conf.get("probability", anomaly_def.get("probability", 1.0))
                        if random.random() < probability:
                            merged_params = {**params, **field_conf}
                            anomaly = anomaly_cls(**merged_params)
                            event[field] = anomaly.apply(event[field])
                            self.anomaly_stats[anomaly_type] += 1
                            event.setdefault("anomalies_applied", []).append(anomaly_type)

        return event

    def apply_to_interaction(self, events: list[dict], interaction_type: str) -> list[dict]:
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
                continue

            anomaly_cls = get_anomaly_class(anomaly_def["type"], "interaction")
            params = anomaly_def.get("params", {})
            anomaly_type = anomaly_def["type"]
            anomaly = anomaly_cls(**params)

            events = anomaly.apply(events)
            self.anomaly_stats[anomaly_type] += 1

            for event in events:
                event.setdefault("anomalies_applied", []).append(anomaly_type)

        return events

    def apply_to_dataset(self, df: pd.DataFrame) -> pd.DataFrame:
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
            anomaly_type = anomaly_def["type"]
            anomaly = anomaly_cls(**params)

            df = anomaly.apply(df)
            self.anomaly_stats[anomaly_type] += 1

            # Optional labeling in DataFrame
            if "dataset_anomaly_applied" not in df.columns:
                df["dataset_anomaly_applied"] = ""

            df["dataset_anomaly_applied"] = df["dataset_anomaly_applied"].astype(str)
            df["dataset_anomaly_applied"] = df["dataset_anomaly_applied"].apply(
                lambda val: f"{val},{anomaly_type}" if val else anomaly_type
            )

        return df

    def get_metrics(self):
        total = sum(self.anomaly_stats.values())
        return {
            "total_anomalies_applied": total,
            "anomalies_count_by_type": dict(self.anomaly_stats),
            "percentage_by_type": {
                k: round(v / total * 100, 2) if total > 0 else 0.0
                for k, v in self.anomaly_stats.items()
            }
        }
