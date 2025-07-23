from agents.a2a_protocol.message_protocol import AgentMessage

class ChurnPatternAgent:
    def __init__(self, data):
        self.data = data

    def detect(self):
        churned = [c for c in self.data if c.get("churned")]
        churn_rate = len(churned) / len(self.data) if self.data else 0
        return {
            "pattern": "churn",
            "churn_rate": churn_rate,
            "num_churned": len(churned)
        }

    def handle_message(self, message: AgentMessage):
        if message.type == "REQUEST_PATTERN":
            return self.detect() 