from interaction_templates.event_template_loader import build_event
from datetime import datetime

def test_build_email_event_received():
    event_type = "email_received"
    interaction_id = "email-test-001"
    timestamp = datetime.utcnow().isoformat()

    event = build_event("email", event_type, interaction_id, timestamp)

    assert "sender_id" in event
    assert "subject_length" in event
    assert isinstance(event["subject_length"], int)

def test_build_email_event_processed():
    event_type = "email_processed"
    interaction_id = "email-test-002"
    timestamp = datetime.utcnow().isoformat()

    event = build_event("email", event_type, interaction_id, timestamp)

    assert "processing_time_ms" in event
    assert isinstance(event["processing_time_ms"], int)

def test_build_email_event_responded():
    event_type = "email_responded"
    interaction_id = "email-test-003"
    timestamp = datetime.utcnow().isoformat()

    event = build_event("email", event_type, interaction_id, timestamp)

    assert "response_time_minutes" in event
    assert "response_sentiment" in event
    assert isinstance(event["response_time_minutes"], int)
    assert isinstance(event["response_sentiment"], float)
