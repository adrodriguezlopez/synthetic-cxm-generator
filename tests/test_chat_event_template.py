from datetime import datetime
from interaction_templates.core.base_event_context import BaseEventContext
from interaction_templates.event_template_loader import build_event

def test_build_chat_event_chat_message():
    context = BaseEventContext(
        interaction_id="chat-test-001",
        timestamp=datetime.utcnow().isoformat(),
        channel="chat",
        event_type="chat_message"
    )

    event = build_event(context)

    assert event["channel"] == "chat"
    assert event["event_type"] == "chat_message"
    assert "message_length" in event
    assert "sentiment_score" in event
