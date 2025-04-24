import random
from interaction_templates.anomalies.base_anomaly import BaseAnomaly

class InteractionMissingEventAnomaly(BaseAnomaly):
    category = "interaction"

    def apply(self, events:list)-> list:
        if not events:
            return events
        drop_index = random.randint(0, len(events) - 1)
        return [e for i, e in enumerate(events) if i != drop_index]