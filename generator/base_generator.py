import uuid
import random
import pandas as pd
from datetime import datetime, timedelta

class BaseGenerator:
    def __init__(self, config: dict, profile: dict):
        """
        Initializes the generator base with the configuration of the scenario
        and the profile of the base behaivior
        """
        self.config = config
        self.profile = profile
        self.channel = config.get("channel", "unknown")
        self.records = []

    def generate_interaction_id(self):
        return str(uuid.uuid4())
    
    def generate_timestamp(self, start_time, offset_seconds):
        return start_time + timedelta(seconds=offset_seconds)
    
    def generate_event(self, interaction_id, timestamp, step):
        """
        Generates a generic event. this method must be overwritten by each channel generator 
        """
        raise NotImplementedError("Subclasses must implement this method")
    
    def run(self, num_interactions: int = 10):
        """
        Executes the generator for a quantity of predefined sessions
        """
        for _ in range(num_interactions):
            interaction_id = self.generate_interaction_id()
            start_time = datetime.now()

            session_length = random.randint(
                self.profile.get("min_events_per_session", 3),
                self.profile.get("max_events_per_session", 5)
            )

            for step in range(session_length):
                timestamp = self.generate_timestamp(start_time, step * self.profile.get("event_spacing_seconds", 1))
                event = self.generate_event(interaction_id, timestamp, step)
                self.records.append(event)
            
    def to_dataframe(self):
        '''
        Returns a dataframe with the generated data
        '''
        return pd.DataFrame(self.records)