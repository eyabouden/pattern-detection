import os
import json
from collections import Counter

class CRMPatternDetectionAgent:
    def __init__(self, data_dir="data/companies/our_company/synthetic_internal/crm_data"):
        self.data_dir = data_dir
        self.crm_data = self.load_crm_data()

    def load_crm_data(self):
        all_data = []
        for year_folder in os.listdir(self.data_dir):
            year_path = os.path.join(self.data_dir, year_folder, "crm_data.json")
            if os.path.exists(year_path):
                with open(year_path) as f:
                    all_data.extend(json.load(f))
        return all_data

    def detect_patterns(self, prompt: str):
        """
        Accepts a prompt and returns pattern analysis.
        """
        prompt = prompt.lower()
        if "churn" in prompt:
            return self.detect_churn_patterns()
        elif "high-value" in prompt or "high value" in prompt:
            return self.find_high_value_clients()
        elif "satisfaction" in prompt:
            return self.satisfaction_trends()
        else:
            return {"error": "Pattern not recognized in prompt."}

    def detect_churn_patterns(self):
        churned = [c for c in self.crm_data if c["churned"]]
        retained = [c for c in self.crm_data if not c["churned"]]
        churn_rate = len(churned) / len(self.crm_data) if self.crm_data else 0
        churn_by_industry = Counter([c["industry"] for c in churned])
        return {
            "pattern": "churn",
            "churn_rate": churn_rate,
            "churn_by_industry": dict(churn_by_industry),
            "num_churned": len(churned),
            "num_retained": len(retained)
        }

    def find_high_value_clients(self, threshold=500000):
        high_value = [c for c in self.crm_data if c["project_value"] >= threshold]
        return {
            "pattern": "high_value_clients",
            "threshold": threshold,
            "clients": high_value[:10]  # Return top 10 for brevity
        }

    def satisfaction_trends(self):
        by_year = {}
        for c in self.crm_data:
            year = c["client_id"][1:5]
            by_year.setdefault(year, []).append(c["satisfaction"])
        avg_by_year = {year: sum(vals)/len(vals) for year, vals in by_year.items()}
        return {
            "pattern": "satisfaction_trends",
            "average_by_year": avg_by_year
        }

# Example usage with prompt engineering
if __name__ == "__main__":
    agent = CRMPatternDetectionAgent()
    prompts = [
        "Find churn patterns in CRM data",
        "Show me high-value clients",
        "What are the satisfaction trends?"
    ]
    for prompt in prompts:
        print(f"\nPrompt: {prompt}")
        result = agent.detect_patterns(prompt)
        print(json.dumps(result, indent=2)) 