import yaml
from schemas.base_event_schema import BASE_EVENT_FIELDS
from interaction_templates.generators.call.base_call_generator import BaseCallFieldGenerator

#load event definitions from Yaml config
with open("config/event_definitions.yaml", "r") as f:
    EVENT_DEFINITIONS = yaml.safe_load(f)

#use the base call field generator
field_generator = BaseCallFieldGenerator()

def build_call_event(event_type: str, interaction_id: str, timestamp: str) -> dict:
    """
    Build a full event for a given interaction step based on the event_type.
    """

    event = BASE_EVENT_FIELDS.copy()

    #set required base fields
    event.update({
        "interaction_id": interaction_id,
        "timestamp": timestamp,
        "channel" : "call",
        "event_type": event_type
    })

    event_template = EVENT_DEFINITIONS.get(event_type, {})
    custom_fields = event_template.get("custom_fields",{})

    #generate each custom field
    for field_name, field_type in custom_fields.items():
        event[field_name] = field_generator.generate(field_name, field_type)

    return event
     