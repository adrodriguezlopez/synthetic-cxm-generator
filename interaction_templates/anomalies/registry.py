from interaction_templates.anomalies.event_level.timestamp_jump import EventTimestampJumpAnomaly
from interaction_templates.anomalies.event_level.extreme_value import EventExtremeValueAnomaly
from interaction_templates.anomalies.interaction_level.missing_event import InteractionMissingEventAnomaly
from interaction_templates.anomalies.dataset_level.duplicate_interaction import DatasetDuplicateInteractionAnomaly


#registry that maps(type, category) -> class
ANOMALY_REGISTRY = {
    ("timestamp_jump", "event"): EventTimestampJumpAnomaly,
    ("extreme_value","event"): EventExtremeValueAnomaly,
    ("missing_event", "interaction"): InteractionMissingEventAnomaly,
    ("duplicate_interaction", "dataset"): DatasetDuplicateInteractionAnomaly
}

def get_anomaly_class(type_name: str, category: str):
    """
    Return the anomaly class given its type and category.
    """
    key = (type_name,category)
    cls = ANOMALY_REGISTRY.get(key)
    if not cls:
        raise ValueError(f"No anomaly class registered for type '{type_name}' and category '{category}'")
    return cls

def get_anomalies_by_category(category: str) -> list:
    """
    Return all anomaly classes for a given category (e.g. 'event', 'interaction').
    """
    return [cls for (t, c), cls in ANOMALY_REGISTRY.items() if c == category]
