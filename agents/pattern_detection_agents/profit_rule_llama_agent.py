import os
import json
from collections import defaultdict
from agents.a2a_protocol.message_protocol import AgentMessage

try:
    from llama_cpp import Llama
    LLAMA_AVAILABLE = True
except ImportError:
    LLAMA_AVAILABLE = False

class ProfitRuleLlamaAgent:
    def __init__(self, data, llama_model_path=None, memory_path="profit_rule_agent_memory.json"):
        self.data = data
        self.llama_model_path = llama_model_path
        self.llama = None
        self.memory_path = memory_path
        self.memory = self.load_memory()
        if LLAMA_AVAILABLE and llama_model_path:
            self.llama = Llama(model_path=llama_model_path, n_ctx=2048)

    def load_memory(self):
        if os.path.exists(self.memory_path):
            with open(self.memory_path, "r") as f:
                return json.load(f)
        return []

    def save_memory(self):
        with open(self.memory_path, "w") as f:
            json.dump(self.memory, f, indent=2)

    def detect_patterns(self, use_llama=True):
        summary = self.summarize_data()
        prompt = (
            "Vous êtes un agent intelligent spécialisé dans la détection de patterns à partir de données internes de projets.\n"
            "Votre tâche est d'analyser le résumé de données de projets ci-dessous et de générer une liste de **règles métier actionnables** basées sur des **patterns fréquents ou significatifs** liés à la **rentabilité et la performance**.\n"
            "🎯 Concentrez-vous sur l'identification de relations statistiques ou logiques pertinentes entre :\n"
            "- type de projet,\n- secteur,\n- composition d'équipe,\n- et autres facteurs pertinents (ex : durée, budget, succès, satisfaction client).\n"
            "✅ Format pour chaque règle :\n"
            "**\"Si [condition détectée], alors [impact observé]\"**\n"
            "📌 Contraintes :\n- Utilisez des valeurs numériques réelles trouvées dans le résumé.\n- Donnez **autant de règles pertinentes que nécessaire** (pas de nombre fixe).\n- Soyez **concis**, **factuel** et **orienté décision**.\n- Répondez **uniquement en français**.\n"
            "---\n\n"
            "📊 **RÉSUMÉ DES DONNÉES DE PROJETS :**\n"
            f"{summary}\n"
        )
        if use_llama and self.llama:
            response = self.llama(prompt, max_tokens=512, stop=["\n\n"])
            rules = response["choices"][0]["text"].strip()
        else:
            rules = self.simple_rule_mining()
        self.memory.append({"prompt": prompt, "rules": rules})
        self.save_memory()
        return {
            "pattern": "profit_rules",
            "rules": rules
        }

    def summarize_data(self):
        summary = []
        groupings = defaultdict(list)
        for p in self.data:
            key = (p["project_type"], p["industry"], p["team_size"])
            groupings[key].append(p["profit"])
        for (ptype, industry, tsize), profits in groupings.items():
            avg_profit = sum(profits) / len(profits)
            summary.append(
                f"{ptype} | {industry} | taille équipe {tsize} : profit moyen {avg_profit:,.0f} sur {len(profits)} projets"
            )
        return "\n".join(summary[:30])

    def simple_rule_mining(self):
        groupings = defaultdict(list)
        for p in self.data:
            key = (p["project_type"], p["industry"], p["team_size"])
            groupings[key].append(p["profit"])
        sorted_groups = sorted(groupings.items(), key=lambda x: sum(x[1])/len(x[1]), reverse=True)
        rules = []
        for (ptype, industry, tsize), profits in sorted_groups[:3]:
            avg_profit = sum(profits) / len(profits)
            rules.append(
                f"Si le projet est '{ptype}' pour '{industry}' avec une équipe de {tsize}, le profit moyen est {avg_profit:,.0f}."
            )
        return "\n".join(rules)

    def fetch_latest_data(self):
        return self.data

    def handle_message(self, message: AgentMessage):
        if message.type == "REQUEST_PATTERN":
            return self.detect_patterns(use_llama=True)
        elif message.type == "FETCH_LATEST_DATA":
            return self.fetch_latest_data()
        elif message.type == "GET_MEMORY":
            return self.memory
        else:
            return {"error": "Unknown message type"}

if __name__ == "__main__":
    with open("data/companies/our_company/synthetic_internal/project_data/2021/project_data.json") as f:
        project_data = json.load(f)
    llama_model_path = "llama-2-7b-chat.ggmlv3.q4_0.bin"  # Update with your model path
    agent = ProfitRuleLlamaAgent(project_data, llama_model_path=llama_model_path)
    result = agent.detect_patterns(use_llama=True)
    print(result["rules"]) 