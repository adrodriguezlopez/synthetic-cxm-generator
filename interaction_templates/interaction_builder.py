import yaml
from datetime import datetime, timedelta

from interaction_templates.core.base_event_context import BaseEventContext
from interaction_templates.core.abstract_event_context import AbstractEventContext
from interaction_templates.event_template_loader import build_event


def generate_interaction(sequence_type: str, context: AbstractEventContext, start_time: datetime = None) -> list:
    """
    Generate a full list of events for a given sequence_type using a given EventContext.
    This is the main recommended interface.
    """
    sequence_path = f"config/{context.channel}_sequences.yaml"

    # Load the correct sequence YAML
    with open(sequence_path, "r") as f:
        sequences = yaml.safe_load(f)

    sequence = sequences.get(sequence_type)
    if not sequence:
        raise ValueError(f"Unknown sequence type '{sequence_type}' for channel '{context.channel}'")

    start_time = start_time or datetime.utcnow()
    events = []

    for step, event_type in enumerate(sequence):
        timestamp = (start_time + timedelta(seconds=step * 10)).isoformat()
        
        # Build a new context per step (same base + updated event_type and timestamp)
        step_context = BaseEventContext(
            interaction_id=context.interaction_id,
            timestamp=timestamp,
            channel=context.channel,
            event_type=event_type,
            **context.extra_fields  # preserve extra context
        )

        event = build_event(step_context)
        events.append(event)

    return events


# Legacy wrapper for backward compatibility
def generate_interaction_legacy(channel: str, sequence_type: str, interaction_id: str, start_time: datetime = None) -> list:
    context = BaseEventContext(
        interaction_id=interaction_id,
        timestamp=(start_time or datetime.utcnow()).isoformat(),
        channel=channel,
        event_type=sequence_type  # placeholder, will be replaced per step
    )
    return generate_interaction(sequence_type=sequence_type, context=context, start_time=start_time)
