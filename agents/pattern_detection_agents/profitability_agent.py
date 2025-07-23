from collections import defaultdict
from agents.a2a_protocol.message_protocol import AgentMessage

class ProfitabilityPatternAgent:
    def __init__(self, data):
        self.data = data

    def detect(self):
        # Group by project type and industry
        profit_by_type = defaultdict(list)
        profit_by_industry = defaultdict(list)
        for p in self.data:
            profit_by_type[p["project_type"]].append(p["profit"])
            profit_by_industry[p["industry"]].append(p["profit"])

        avg_profit_type = {k: sum(v)/len(v) for k, v in profit_by_type.items()}
        avg_profit_industry = {k: sum(v)/len(v) for k, v in profit_by_industry.items()}

        # Find the best and worst project types/industries
        best_type = max(avg_profit_type, key=avg_profit_type.get)
        worst_type = min(avg_profit_type, key=avg_profit_type.get)
        best_industry = max(avg_profit_industry, key=avg_profit_industry.get)
        worst_industry = min(avg_profit_industry, key=avg_profit_industry.get)

        # Simple profit equation (linear regression would be better, but for demo:)
        avg_margin = sum([p["profit_margin"] for p in self.data]) / len(self.data)
        equation = f"Profit ≈ {avg_margin:.2f} × Revenue"

        summary = (
            f"Most profitable project type: {best_type} (avg profit: {avg_profit_type[best_type]:,.0f})\n"
            f"Least profitable project type: {worst_type} (avg profit: {avg_profit_type[worst_type]:,.0f})\n"
            f"Most profitable industry: {best_industry} (avg profit: {avg_profit_industry[best_industry]:,.0f})\n"
            f"Least profitable industry: {worst_industry} (avg profit: {avg_profit_industry[worst_industry]:,.0f})\n"
            f"General profit equation: {equation}"
        )

        return {
            "pattern": "profitability",
            "summary": summary,
            "avg_profit_by_type": avg_profit_type,
            "avg_profit_by_industry": avg_profit_industry,
            "equation": equation
        }

    def handle_message(self, message: AgentMessage):
        if message.type == "REQUEST_PATTERN":
            return self.detect() 