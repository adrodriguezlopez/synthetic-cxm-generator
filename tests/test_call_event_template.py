from datetime import datetime
from interaction_templates.core.base_event_context import BaseEventContext
from interaction_templates.event_template_loader import build_event

def test_build_call_event_call_started():
    context = BaseEventContext(
        interaction_id="test-001",
        timestamp=datetime.utcnow().isoformat(),
        channel="call",
        event_type="call_started"
    )

    event = build_event(context)

    assert isinstance(event, dict)
    assert event["channel"] == "call"
    assert event["event_type"] == "call_started"
    assert "agent_id" in event
    assert "customer_id" in event
