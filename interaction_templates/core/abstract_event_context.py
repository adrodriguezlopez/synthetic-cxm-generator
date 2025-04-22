from abc import ABC, abstractmethod

class AbstractEventContext(ABC):
    @abstractmethod
    def to_dict(self) -> dict:
        """
        Return a dictionary with all fields available for event generation.
        """
        pass
