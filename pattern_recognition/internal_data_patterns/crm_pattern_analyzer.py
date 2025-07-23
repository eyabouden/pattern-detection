import os
import json
from collections import Counter

def load_crm_data(base_dir="data/companies/our_company/synthetic_internal/crm_data"):
    all_data = []
    for year_folder in os.listdir(base_dir):
        year_path = os.path.join(base_dir, year_folder, "crm_data.json")
        if os.path.exists(year_path):
            with open(year_path) as f:
                all_data.extend(json.load(f))
    return all_data

def detect_churn_patterns(crm_data):
    churned = [c for c in crm_data if c["churned"]]
    retained = [c for c in crm_data if not c["churned"]]
    churn_rate = len(churned) / len(crm_data) if crm_data else 0
    churn_by_industry = Counter([c["industry"] for c in churned])
    return {
        "churn_rate": churn_rate,
        "churn_by_industry": churn_by_industry,
        "num_churned": len(churned),
        "num_retained": len(retained)
    }

def find_high_value_clients(crm_data, threshold=500000):
    return [c for c in crm_data if c["project_value"] >= threshold]

def satisfaction_trends(crm_data):
    by_year = {}
    for c in crm_data:
        year = c["client_id"][1:5]
        by_year.setdefault(year, []).append(c["satisfaction"])
    avg_by_year = {year: sum(vals)/len(vals) for year, vals in by_year.items()}
    return avg_by_year

def main():
    crm_data = load_crm_data()
    print("Loaded", len(crm_data), "CRM records.")

    churn_patterns = detect_churn_patterns(crm_data)
    print("\nChurn Patterns:")
    print(f"  Churn rate: {churn_patterns['churn_rate']:.2%}")
    print(f"  Churned by industry: {dict(churn_patterns['churn_by_industry'])}")
    print(f"  Number churned: {churn_patterns['num_churned']}")
    print(f"  Number retained: {churn_patterns['num_retained']}")

    high_value = find_high_value_clients(crm_data)
    print(f"\nHigh-value clients (project_value >= 500,000): {len(high_value)}")
    for c in high_value[:5]:
        print(f"  {c['client_name']} ({c['project_value']})")

    trends = satisfaction_trends(crm_data)
    print("\nAverage satisfaction by year:")
    for year, avg in trends.items():
        print(f"  {year}: {avg:.2f}")

if __name__ == "__main__":
    main() 