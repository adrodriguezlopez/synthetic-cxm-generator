from datetime import datetime
from interaction_templates.core.base_event_context import BaseEventContext
from interaction_templates.interaction_builder import generate_interaction_stream

def test_stream_yields_correct_number_of_events():
    context = BaseEventContext(
        interaction_id="test-stream-001",
        timestamp=datetime.utcnow().isoformat(),
        channel="call",
        event_type="placeholder"
    )
    events = list(generate_interaction_stream("standard", context))
    assert len(events) == 3  # call_normal has 3 events

def test_stream_event_structure_is_valid():
    context = BaseEventContext(
        interaction_id="test-stream-002",
        timestamp=datetime.utcnow().isoformat(),
        channel="call",
        event_type="placeholder"
    )
    for event in generate_interaction_stream("standard", context):
        assert "interaction_id" in event
        assert "timestamp" in event
        assert "channel" in event
        assert "event_type" in event

def test_stream_event_type_sequence():
    context = BaseEventContext(
        interaction_id="test-stream-003",
        timestamp=datetime.utcnow().isoformat(),
        channel="call",
        event_type="placeholder"
    )
    expected = ["call_started", "call_active", "call_ended"]
    result = [e["event_type"] for e in generate_interaction_stream("standard", context)]
    assert result == expected

def test_stream_timestamps_progress_correctly():
    context = BaseEventContext(
        interaction_id="test-stream-004",
        timestamp=datetime.utcnow().isoformat(),
        channel="call",
        event_type="placeholder"
    )
    timestamps = [e["timestamp"] for e in generate_interaction_stream("standard", context)]
    dts = [datetime.fromisoformat(ts) for ts in timestamps]
    deltas = [(dts[i+1] - dts[i]).total_seconds() for i in range(len(dts)-1)]
    assert all(8 <= d <= 12 for d in deltas)  # ~10 seconds, allowing small drift
