from agents.a2a_protocol.message_protocol import AgentMessage

class RepeatClientPatternAgent:
    def __init__(self, data):
        self.data = data

    def detect(self):
        repeat = [p for p in self.data if p["is_repeat_client"]]
        new = [p for p in self.data if not p["is_repeat_client"]]
        avg_profit_repeat = sum([p["profit"] for p in repeat]) / len(repeat) if repeat else 0
        avg_profit_new = sum([p["profit"] for p in new]) / len(new) if new else 0

        summary = (
            f"Repeat clients: {len(repeat)} projects, avg profit: {avg_profit_repeat:,.0f}\n"
            f"New clients: {len(new)} projects, avg profit: {avg_profit_new:,.0f}\n"
            f"Repeat clients are {'more' if avg_profit_repeat > avg_profit_new else 'less'} profitable on average."
        )

        return {
            "pattern": "repeat_clients",
            "summary": summary,
            "avg_profit_repeat": avg_profit_repeat,
            "avg_profit_new": avg_profit_new
        }

    def handle_message(self, message: AgentMessage):
        if message.type == "REQUEST_PATTERN":
            return self.detect() 