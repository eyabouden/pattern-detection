from collections import defaultdict, Counter
from agents.a2a_protocol.message_protocol import AgentMessage

class ERPPatternAgent:
    def __init__(self, data):
        self.data = data

    def detect(self):
        # Group by department and project type
        delay_patterns = defaultdict(list)
        for r in self.data:
            key = (r["department"], r["project"])
            delay_patterns[key].append(r["status"] == "Delayed")

        rules = []
        for (dept, project), statuses in delay_patterns.items():
            if len(statuses) >= 3:
                delay_rate = sum(statuses) / len(statuses)
                if delay_rate > 0.5:
                    rules.append(
                        f"Si le projet '{project}' est mené par le département '{dept}', le risque de retard est de {int(delay_rate*100)}% ({sum(statuses)}/{len(statuses)} projets)."
                    )
        if not rules:
            rules = ["Aucun pattern de risque de retard significatif détecté."]
        return {
            "pattern": "erp_delay_rules",
            "rules": rules
        }

    def handle_message(self, message: AgentMessage):
        if message.type == "REQUEST_PATTERN":
            return self.detect() 