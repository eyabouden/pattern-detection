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
        # Seasonality: more projects in Q2/Q4, more delays in summer
        month_weights = [0.08, 0.09, 0.12, 0.13, 0.10, 0.08, 0.07, 0.07, 0.09, 0.10, 0.12, 0.13]
        project_month = random.choices(range(1, 13), weights=month_weights)[0]
        status = random.choices(PROJECT_STATUS, weights=[0.7, 0.2, 0.1] if project_month in [6,7,8] else [0.5,0.4,0.1])[0]
        department = random.choice(CONSULTING_DEPARTMENTS)
        project = random.choice(PROJECTS)
        # Correlation: higher cost for certain projects/departments
        base_cost = random.uniform(20000, 800000)
        if project in ["SAP Rollout", "Cloud Migration"]:
            base_cost *= 1.2
        if department == "Technology":
            base_cost *= 1.1
        # Anomaly: rare very high cost
        if random.random() < 0.02:
            base_cost *= random.uniform(2, 3)
        cost = round(base_cost, 2)
        # Duration: longer for delayed projects
        duration_months = random.randint(2, 18)
        if status == "Delayed":
            duration_months += random.randint(1, 6)
        # Cross-dataset: simulate impact of financial stress (e.g., more delays if previous year had high expenses)
        if year > 2021 and random.random() < 0.05:
            status = "Delayed"
        record = {
            "record_id": f"E{year}{i:03d}",
            "department": department,
            "project": project,
            "cost": cost,
            "status": status,
            "duration_months": duration_months,
            "project_month": project_month
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