from interaction_templates.utils.config_loader import (
    load_event_definitions,
    BaseEventFields
)

from interaction_templates.generators.call.base_call_generator import BaseCallFieldGenerator
from interaction_templates.generators.chat.chat_field_generator import BaseChatFieldGenerator
from interaction_templates.generators.email.email_field_generator import BaseEmailFieldGenerator
from interaction_templates.core.abstract_event_context import AbstractEventContext

# Load all event definitions (from config/event_definitions/*.yaml)
EVENT_DEFINITIONS = load_event_definitions()

# Load base event schema (from config/base_event_fields.yaml)
base_event_fields = BaseEventFields()

# Map of field generators per channel
GENERATOR_MAP = {
    "call": BaseCallFieldGenerator(),
    "chat": BaseChatFieldGenerator(),
    "email": BaseEmailFieldGenerator()
}

def build_event(context: AbstractEventContext) -> dict:
    """
    Build a complete event using the provided context object.
    The context must implement .to_dict() and contain all relevant fields.
    """
    event_type = context.event_type
    channel = context.channel

    generator = GENERATOR_MAP.get(channel)
    if not generator:
        raise ValueError(f"No generator defined for channel '{channel}'")

    # Build base fields using the schema and context
    event = base_event_fields.build(context)

    # Load additional custom fields from YAML
    event_template = EVENT_DEFINITIONS.get(event_type, {})
    custom_fields = event_template.get("custom_fields", {})

    for field_name, field_type in custom_fields.items():
        event[field_name] = generator.generate(field_name, field_type)

    return event
