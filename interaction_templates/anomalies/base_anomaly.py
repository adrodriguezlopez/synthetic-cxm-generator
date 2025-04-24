from abc import ABC, abstractmethod

class BaseAnomaly(ABC):
    """
    Abstract base class for all anomaly types.
    """

    category = "event" #Default: can be 'event', 'interaction', 'dataset', etc

    def __init__(self, **params):
        self.params = params # Parameters for YAML or injector

    @abstractmethod
    def apply(self, *args, **kwargs):
        """
        Apply the anomaly, Subclases must implement this.
        Can be used on a value, an event, or a list of events, or a dataset
        """
        pass