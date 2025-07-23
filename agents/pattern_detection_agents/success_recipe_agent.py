from collections import defaultdict
from agents.a2a_protocol.message_protocol import AgentMessage

class SuccessRecipeAgent:
    def __init__(self, data):
        self.data = data

    def detect(self):
        # Define "success" as profit margin > 0.25
        recipes = defaultdict(list)
        for p in self.data:
            key = (
                p["project_type"],
                p["industry"],
                tuple(sorted(set(p["team_roles"]))),
            )
            is_success = p["profit_margin"] > 0.25
            recipes[key].append(is_success)

        best_patterns = []
        for key, results in recipes.items():
            success_rate = sum(results) / len(results)
            if len(results) >= 5 and success_rate > 0.8:
                project_type, industry, team_roles = key
                team_roles_str = ", ".join(team_roles)
                best_patterns.append(
                    f"Une offre de {project_type} pour {industry}, avec une équipe composée de {team_roles_str}, a eu {int(success_rate*100)}% de succès (profit margin > 25%) sur {len(results)} projets."
                )

        if not best_patterns:
            best_patterns.append("Aucun pattern de succès fort n'a été détecté dans les données.")

        return {
            "pattern": "success_recipes",
            "recipes": best_patterns
        }

    def handle_message(self, message: AgentMessage):
        if message.type == "REQUEST_PATTERN":
            return self.detect() 