from datetime import datetime
import pandas as pd
from interaction_templates.core.base_event_context import BaseEventContext
from interaction_templates.interaction_builder import generate_interaction
from interaction_templates.anomalies.injector import AnomalyInjector

# === Parameters ===
interaction_type = "call_transfer"
channel = "call"
cxm = "CXM1"
inject_anomalies = True
output_path = "datasets/generated_with_anomalies.csv"
config_path = "config/anomaly_profiles/test_profile.yaml"

# === Generate context and events ===
context = BaseEventContext(
    interaction_id="test-001",
    timestamp=datetime.utcnow().isoformat(),
    channel=channel,
    event_type="placeholder"
)

# === Generate clean interaction ===
events = generate_interaction(sequence_type=interaction_type, context=context)

# === Apply anomalies if enabled ===
if inject_anomalies:
    injector = AnomalyInjector(config_path=config_path, cxm=cxm)
    events = injector.apply_to_interaction(events, interaction_type=interaction_type)
    events = [injector.apply_to_event(e, e["event_type"]) for e in events]

# === Export to CSV ===
df = pd.DataFrame(events)
df.to_csv(output_path, index=False)

print(f"✅ Interaction generated and saved to {output_path}")
