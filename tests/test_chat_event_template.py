from interaction_templates.event_template_loader import build_event
from datetime import datetime

def test_build_chat_event_chat_started():
    event_type = "chat_started"
    interaction_id = "chat-test-123"
    timestamp = datetime.utcnow().isoformat()

    event = build_event("chat", event_type, interaction_id, timestamp)

    assert isinstance(event, dict)
    assert event["interaction_id"] == interaction_id
    assert event["timestamp"] == timestamp
    assert event["channel"] == "chat"
    assert event["event_type"] == event_type
    assert "agent_id" in event
    assert "customer_id" in event

def test_build_chat_event_chat_message():
    event_type = "chat_message"
    interaction_id = "chat-test-456"
    timestamp = datetime.utcnow().isoformat()

    event = build_event("chat", event_type, interaction_id, timestamp)

    assert "message_length" in event
    assert "sentiment_score" in event
    assert isinstance(event["message_length"], int)
    assert isinstance(event["sentiment_score"], float)

def test_build_chat_event_chat_ended():
    event_type = "chat_ended"
    interaction_id = "chat-test-789"
    timestamp = datetime.utcnow().isoformat()

    event = build_event("chat", event_type, interaction_id, timestamp)

    assert "end_reason" in event
    assert isinstance(event["end_reason"], str)


