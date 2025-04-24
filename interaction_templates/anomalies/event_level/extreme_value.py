from interaction_templates.anomalies.base_anomaly import BaseAnomaly

class EventExtremeValueAnomaly(BaseAnomaly):
    category = "event"

    def apply(self, value):
        multiplier = self.params.get("multiplier", 10)
        try:
            return float(value) * multiplier
        except:
            return value  # if not numeric, return unchanged
