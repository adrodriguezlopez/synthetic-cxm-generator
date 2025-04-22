from interaction_templates.generators.base_field_generator import BaseFieldGenerator
import random

class BaseChatFieldGenerator(BaseFieldGenerator):

    def generate_agent_id(self):
        return f"chat_agent_{random.randint(100, 999)}"

    def generate_customer_id(self):
        return f"chat_user_{random.randint(1000, 9999)}"

    def generate_message_length(self):
        return random.randint(5, 500)  # characters

    def generate_sentiment_score(self):
        return round(random.uniform(-1.0, 1.0), 3)

    def generate_reason(self):
        return random.choice(["angry_customer", "technical_issue", "escalated_policy"])

    def generate_end_reason(self):
        return random.choice(["user_closed", "timeout", "resolved"])
