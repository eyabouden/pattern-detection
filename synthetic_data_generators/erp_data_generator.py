import random
import json
import os

CONSULTING_DEPARTMENTS = [
    "Consulting", "Technology", "Digital", "Delivery", "Operations"
]
PROJECTS = [
    "SAP Rollout", "Salesforce Integration", "Cloud Migration", "Data Lake Implementation",
    "Agile Transformation", "Cybersecurity Upgrade", "AI Chatbot Deployment", "RPA Automation"
]
PROJECT_STATUS = ["Completed", "Ongoing", "Delayed"]


def generate_synthetic_erp_data(year, num_records=50):
    data = []
    for i in range(num_records):
        record = {
            "record_id": f"E{year}{i:03d}",
            "department": random.choice(CONSULTING_DEPARTMENTS),
            "project": random.choice(PROJECTS),
            "cost": round(random.uniform(20000, 800000), 2),
            "status": random.choice(PROJECT_STATUS),
            "duration_months": random.randint(2, 18)
        }
        data.append(record)
    return data

def save_erp_data(year, data, base_dir="data/companies/our_company/synthetic_internal/erp_data"):
    os.makedirs(f"{base_dir}/{year}", exist_ok=True)
    with open(f"{base_dir}/{year}/erp_data.json", "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    for year in range(2021, 2025):
        data = generate_synthetic_erp_data(year)
        save_erp_data(year, data) 