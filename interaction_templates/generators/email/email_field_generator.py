from interaction_templates.generators.base_field_generator import BaseFieldGenerator
import random

class BaseEmailFieldGenerator(BaseFieldGenerator):

    def generate_sender_id(self):
        return f"email_user_{random.randint(1000, 9999)}"

    def generate_subject_length(self):
        return random.randint(5, 120)

    def generate_processing_time_ms(self):
        return random.randint(100, 5000)

    def generate_response_time_minutes(self):
        return random.randint(1, 60)

    def generate_response_sentiment(self):
        return round(random.uniform(-1.0, 1.0), 3)
