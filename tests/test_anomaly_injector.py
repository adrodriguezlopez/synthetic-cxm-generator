import pytest
import pandas as pd
from datetime import datetime
from interaction_templates.anomalies.injector import AnomalyInjector
@pytest.fixture
def injector():
    return AnomalyInjector(config_path="config/anomaly_profiles/test_profile.yaml", cxm="CXM1")

def test_apply_to_event_timestamp_jump(injector):
    event = {
        "interaction_id": "int001",
        "event_type": "call_active",
        "timestamp": "2025-04-23T10:00:00"
    }
    modified = injector.apply_to_event(event.copy(), event_type="call_active")
    assert modified["timestamp"] != event["timestamp"]
    assert "T" in modified["timestamp"]

def test_apply_to_interaction_missing_event(injector):
    interaction = [
        {"interaction_id": "int002", "event_type": "call_started", "timestamp": "2025-04-23T10:00:00"},
        {"interaction_id": "int002", "event_type": "call_active", "timestamp": "2025-04-23T10:00:10"},
        {"interaction_id": "int002", "event_type": "call_ended", "timestamp": "2025-04-23T10:00:20"}
    ]
    modified = injector.apply_to_interaction(interaction.copy(), interaction_type="call_transfer")
    assert len(modified) == len(interaction) - 1

def test_apply_to_dataset_duplicate_interaction(injector):
    dataset = pd.DataFrame([
        {"interaction_id": "int003", "event_type": "call_started", "timestamp": "2025-04-23T11:00:00"},
        {"interaction_id": "int003", "event_type": "call_active", "timestamp": "2025-04-23T11:00:10"},
        {"interaction_id": "int003", "event_type": "call_ended", "timestamp": "2025-04-23T11:00:20"},
        {"interaction_id": "int004", "event_type": "call_started", "timestamp": "2025-04-23T12:00:00"},
        {"interaction_id": "int004", "event_type": "call_ended", "timestamp": "2025-04-23T12:00:20"}
    ])
    modified = injector.apply_to_dataset(dataset.copy())
    assert len(modified) > len(dataset)
    duplicated_ids = modified["interaction_id"].value_counts()
    assert any(count > 3 for count in duplicated_ids.values)
