import yaml
from schemas.base_event_schema import BASE_EVENT_FIELDS
from interaction_templates.generators.call.base_call_generator import BaseCallFieldGenerator
from interaction_templates.generators.chat.chat_field_generator import BaseChatFieldGenerator
from interaction_templates.generators.email.email_field_generator import BaseEmailFieldGenerator

# Load shared event definitions
with open("config/event_definitions.yaml", "r") as f:
    EVENT_DEFINITIONS = yaml.safe_load(f)

GENERATOR_MAP = {
    "call": BaseCallFieldGenerator(),
    "chat": BaseChatFieldGenerator(),
    "email": BaseEmailFieldGenerator()
}

def build_event(channel: str, event_type: str, interaction_id: str, timestamp: str) ->dict:
    generator = GENERATOR_MAP.get(channel)
    if not generator:
        raise ValueError(f"No generator defined for channel '{channel}'")
    
    event = BASE_EVENT_FIELDS.copy()
    event.update({
        "interaction_id": interaction_id,
        "timestamp": timestamp,
        "channel": channel,
        "event_type": event_type
    })

    #Get custom fields from events_definitions.yaml
    event_template = EVENT_DEFINITIONS.get(event_type, {})
    custom_fields = event_template.get("custom_fields",{})

    for field_name, field_type in custom_fields.items():
        print("CALLING:", field_name, field_type, generator)
        event[field_name] = generator.generate(field_name, field_type)

    return event