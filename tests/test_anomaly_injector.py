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

def test_event_has_anomalies_applied_field(injector):
    event = {
        "interaction_id": "int010",
        "event_type": "call_active",
        "timestamp": "2025-04-23T10:00:00"
    }
    modified = injector.apply_to_event(event.copy(), event_type="call_active")
    assert "anomalies_applied" in modified
    assert isinstance(modified["anomalies_applied"], list)
    assert "timestamp_jump" in modified["anomalies_applied"]

def test_get_metrics_returns_correct_summary(injector):
    interaction = [
        {"interaction_id": "int011", "event_type": "call_started", "timestamp": "2025-04-23T10:00:00"},
        {"interaction_id": "int011", "event_type": "call_active", "timestamp": "2025-04-23T10:00:10"},
        {"interaction_id": "int011", "event_type": "call_ended", "timestamp": "2025-04-23T10:00:20"}
    ]
    injector.apply_to_interaction(interaction, interaction_type="call_transfer")
    for event in interaction:
        injector.apply_to_event(event, event_type=event["event_type"])

    metrics = injector.get_metrics()
    assert "total_anomalies_applied" in metrics
    assert metrics["total_anomalies_applied"] > 0
    assert "timestamp_jump" in metrics["anomalies_count_by_type"]
    assert "missing_event" in metrics["anomalies_count_by_type"]

def test_multiple_anomalies_applied_to_single_event(injector):
    event = {
        "interaction_id": "int012",
        "event_type": "call_active",
        "timestamp": "2025-04-23T10:00:00",
        "duration_seconds": 120
    }

    modified = injector.apply_to_event(event.copy(), event_type="call_active")

    assert "anomalies_applied" in modified
    assert isinstance(modified["anomalies_applied"], list)
    assert "timestamp_jump" in modified["anomalies_applied"]
    assert "extreme_value" in modified["anomalies_applied"]
    assert modified["timestamp"] != event["timestamp"]
    assert modified["duration_seconds"] != event["duration_seconds"]


