import yaml
from datetime import datetime, timedelta
from interaction_templates.event_template_loader import build_event

def generate_interaction(channel:str, sequence_type:str, interaction_id: str, start_time: datetime= None) -> list:
    """
    Generate a full interaction (list of events) for a given channel and sequence type.
    """
    sequence_path = f"config/{channel}_sequences.yaml"

    # Load YAML sequence for the channel
    with open(sequence_path, "r") as f:
        sequences = yaml.safe_load(f)

    sequence = sequences.get(sequence_type)
    if not sequence:
        raise ValueError(f"Unknown sequence type '{sequence_type}' for channel '{channel}'")
    
    start_time = start_time or datetime.utcnow()
    events = []

    for step, event_type in enumerate(sequence):
        timestamp = (start_time + timedelta(seconds=step*10)).isoformat()
        event= build_event(channel, event_type, interaction_id, timestamp)
        events.append(event)

    return events