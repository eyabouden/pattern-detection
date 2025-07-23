from collections import defaultdict
from agents.a2a_protocol.message_protocol import AgentMessage

class FinancialPatternAgent:
    def __init__(self, data):
        self.data = data

    def detect(self):
        # Group by client and month
        profit_patterns = defaultdict(list)
        for f in self.data:
            key = (f.get("client", "Unknown"), f["month"])
            profit_patterns[key].append(f["profit"])

        rules = []
        for (client, month), profits in profit_patterns.items():
            if len(profits) >= 2:
                avg_profit = sum(profits) / len(profits)
                if avg_profit > 150000:
                    rules.append(
                        f"Si le client est '{client}' et le mois est {month}, le profit moyen est élevé: {avg_profit:,.0f}."
                    )
        if not rules:
            rules = ["Aucun pattern de profit élevé détecté."]
        return {
            "pattern": "financial_profit_rules",
            "rules": rules
        }

    def handle_message(self, message: AgentMessage):
        if message.type == "REQUEST_PATTERN":
            return self.detect() 