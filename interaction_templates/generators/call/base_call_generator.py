from ..base_field_generator import BaseFieldGenerator
import random

class BaseCallFieldGenerator(BaseFieldGenerator):
    
    def generate_agent_id(self):
        return f"agent_{random.randint(100,999)}"
    
    def generate_customer_id(self):
        return f"agent_{random.randint(1000, 9999)}"
    
    def generate_duration_seconds(self):
        return random.randint(30,180)
    
    def generate_end_reason(self):
        return random.choice(["user_hangup", "network_drop", "timeout"])
    
    def generate_hold_reason(self):
        return random.choice(["info_lookup", "transfer", "escalation"])

    def generate_reason(self):
        return random.choice(["rejected", "busy", "no_answer"])

    def generate_interaction_type(self):
        return random.choice(["inbound", "outbound"])
