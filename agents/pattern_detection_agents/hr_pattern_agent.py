from collections import defaultdict
from agents.a2a_protocol.message_protocol import AgentMessage

class HRPatternAgent:
    def __init__(self, data):
        self.data = data

    def detect(self):
        # Group by role and tenure
        turnover_patterns = defaultdict(list)
        for e in self.data:
            key = (e["role"], "junior" if e["years_at_company"] < 2 else "senior")
            turnover_patterns[key].append(e["left_company"])

        rules = []
        for (role, seniority), lefts in turnover_patterns.items():
            if len(lefts) >= 3:
                rate = sum(lefts) / len(lefts)
                if rate > 0.5:
                    rules.append(
                        f"Si le rôle est '{role}' ({seniority}), le taux de départ est de {int(rate*100)}% ({sum(lefts)}/{len(lefts)} employés)."
                    )
        if not rules:
            rules = ["Aucun pattern de turnover significatif détecté."]
        return {
            "pattern": "hr_turnover_rules",
            "rules": rules
        }

    def handle_message(self, message: AgentMessage):
        if message.type == "REQUEST_PATTERN":
            return self.detect() 