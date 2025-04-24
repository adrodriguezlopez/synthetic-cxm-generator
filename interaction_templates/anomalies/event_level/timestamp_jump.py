from datetime import datetime, timedelta
from interaction_templates.anomalies.base_anomaly import BaseAnomaly

class EventTimestampJumpAnomaly(BaseAnomaly):
    category = "event"

    def apply(self, value: str) -> str:
        original_timestamp = datetime.fromisoformat(value)
        offset_minutes = self.params.get("minutes",60)
        modified_timestamp = original_timestamp + timedelta(minutes=offset_minutes)
        return modified_timestamp.isoformat()