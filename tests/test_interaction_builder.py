from datetime import datetime
from interaction_templates.interaction_builder import generate_interaction
from interaction_templates.core.base_event_context import BaseEventContext


def test_generate_interaction_call_standard():
    context = BaseEventContext(
        interaction_id="call-001",
        timestamp=datetime.utcnow().isoformat(),
        channel="call",
        event_type="placeholder"  # será reemplazado por cada paso
    )
    events = generate_interaction(sequence_type="standard", context=context)

    assert isinstance(events, list)
    assert len(events) == 3
    assert all(event["channel"] == "call" for event in events)


def test_generate_interaction_chat_standard():
    context = BaseEventContext(
        interaction_id="chat-001",
        timestamp=datetime.utcnow().isoformat(),
        channel="chat",
        event_type="placeholder"
    )
    events = generate_interaction(sequence_type="standard", context=context)

    assert isinstance(events, list)
    assert len(events) == 3
    assert all(event["channel"] == "chat" for event in events)


def test_generate_interaction_email_basic():
    context = BaseEventContext(
        interaction_id="email-001",
        timestamp=datetime.utcnow().isoformat(),
        channel="email",
        event_type="placeholder"
    )
    events = generate_interaction(sequence_type="basic", context=context)

    assert isinstance(events, list)
    assert len(events) == 3
    assert all(event["channel"] == "email" for event in events)
