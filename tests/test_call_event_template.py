import yaml
from interaction_templates.call_event_template import build_call_event
from datetime import datetime, timedelta

with open("config/call_sequences.yaml", 'r') as f:
    CALL_SEQUENCES = yaml.safe_load(f)

def test_build_call_events_returns_complete_event():
    event_type = "call_started"
    interaction_id = "test-interaction_id"
    timestamp = datetime.utcnow().isoformat()

    event = build_call_event(event_type, interaction_id, timestamp)

    assert isinstance(event, dict)
    assert event["interaction_id"] == interaction_id
    assert event["timestamp"] == timestamp
    assert event["channel"] == "call"
    assert event["event_type"] == event_type

    assert "agent_id" in event
    assert "customer_id" in event
    assert isinstance(event["agent_id"], str)
    assert isinstance(event["customer_id"], str)


def test_generate_full_call_interaction_sequence_standard():
    sequence_type = "standard"
    interaction_id = "test-full-interaction-standard"
    start_time = datetime.utcnow()

    sequence = CALL_SEQUENCES.get(sequence_type)
    assert sequence is not None, "Sequence type not found in YAML."
    
    events = []

    for step, event_type in enumerate(sequence):
        timestamp = (start_time + timedelta(seconds=step *10)).isoformat()
        event = build_call_event(event_type,interaction_id,timestamp)
        events.append(event)

    assert len(events) == len(sequence)
    for idx, event in enumerate(events):
        assert event["interaction_id"] == interaction_id
        assert event["channel"] == "call"
        assert event["event_type"] == sequence[idx]