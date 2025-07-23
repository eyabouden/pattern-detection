from collections import Counter
from agents.a2a_protocol.message_protocol import AgentMessage

class SeasonalityPatternAgent:
    def __init__(self, data):
        self.data = data

    def detect(self):
        months = [p["sales_month"] for p in self.data]
        month_counts = Counter(months)
        return {
            "pattern": "seasonality",
            "month_distribution": dict(month_counts)
        }

    def handle_message(self, message: AgentMessage):
        if message.type == "REQUEST_PATTERN":
            return self.detect() 