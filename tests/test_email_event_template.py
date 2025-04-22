from datetime import datetime
from interaction_templates.core.base_event_context import BaseEventContext
from interaction_templates.event_template_loader import build_event

def test_build_email_event_email_received():
    context = BaseEventContext(
        interaction_id="email-test-001",
        timestamp=datetime.utcnow().isoformat(),
        channel="email",
        event_type="email_received"
    )

    event = build_event(context)

    assert event["channel"] == "email"
    assert event["event_type"] == "email_received"
    assert "sender_id" in event
    assert "subject_length" in event
