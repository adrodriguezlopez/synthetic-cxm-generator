from interaction_templates.interaction_builder import generate_interaction
from datetime import datetime

def test_generate_interaction_call_standard():
    interaction_id = "test-call-interaction-standard"
    events = generate_interaction(channel="call", sequence_type="standard", interaction_id=interaction_id)

    assert isinstance(events, list)
    assert len(events) == 3 #expected: start, active, end
    for event in events: 
        assert event["interaction_id"] == interaction_id
        assert event["channel"] == "call"
        assert "timestamp" in event
        assert "event_type" in event


def test_generate_interaction_chat_standard():
    interaction_id = "test-chat-001"
    events = generate_interaction(channel="chat", sequence_type="standard", interaction_id=interaction_id)

    assert isinstance(events, list)
    assert len(events) == 3  # chat_started → chat_message → chat_ended

    expected_event_types = ["chat_started", "chat_message", "chat_ended"]
    expected_fields = {
        "chat_started": ["agent_id", "customer_id"],
        "chat_message": ["message_length", "sentiment_score"],
        "chat_ended": ["end_reason"]
    }

    for idx, event in enumerate(events):
        assert event["interaction_id"] == interaction_id
        assert event["channel"] == "chat"
        assert event["event_type"] == expected_event_types[idx]

        for field in expected_fields.get(event["event_type"], []):
            assert field in event, f"{field} not found in {event['event_type']}"


def test_generate_interaction_email_basic():
    interaction_id = "email-full-001"
    events = generate_interaction(channel="email", sequence_type="basic", interaction_id=interaction_id)

    assert isinstance(events, list)
    assert len(events) == 3  # email_received → email_processed → email_responded

    expected_event_types = ["email_received", "email_processed", "email_responded"]
    expected_fields = {
        "email_received": ["sender_id", "subject_length"],
        "email_processed": ["processing_time_ms"],
        "email_responded": ["response_time_minutes", "response_sentiment"]
    }

    for idx, event in enumerate(events):
        assert event["interaction_id"] == interaction_id
        assert event["channel"] == "email"
        assert event["event_type"] == expected_event_types[idx]

        for field in expected_fields.get(event["event_type"], []):
            assert field in event

