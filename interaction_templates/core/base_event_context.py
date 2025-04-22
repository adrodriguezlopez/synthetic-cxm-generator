from .abstract_event_context import AbstractEventContext

class BaseEventContext(AbstractEventContext):
    def __init__(self, interaction_id, timestamp, channel, event_type, **extra_fields):
        self.interaction_id = interaction_id
        self.timestamp = timestamp
        self.channel = channel
        self.event_type = event_type
        self.extra_fields = extra_fields or {}

    def to_dict(self):
        return {
            "interaction_id": self.interaction_id,
            "timestamp": self.timestamp,
            "channel": self.channel,
            "event_type": self.event_type,
            **self.extra_fields
        }
