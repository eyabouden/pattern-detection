# synthetic_data_generators/crm_data_generator.py

import random
import json
import os

CONSULTING_CLIENTS = [
    "BNP Paribas", "AXA", "EDF", "SNCF", "Orange", "L'Oréal", "Renault", "TotalEnergies",
    "Société Générale", "Airbus", "Sanofi", "Carrefour", "Veolia", "ENGIE", "La Poste"
]
PROJECT_TYPES = [
    "Digital Transformation", "ERP Implementation", "Data Analytics", "Cloud Migration",
    "Cybersecurity Audit", "Process Optimization", "AI/ML Deployment", "IT Outsourcing"
]
INDUSTRIES = [
    "Banking", "Insurance", "Energy", "Public Sector", "Telecom", "Retail", "Pharma", "Transport"
]

def generate_synthetic_crm_data(year, clients):
    data = []
    for client in clients:
        client_id = client["client_id"]
        client_name = client["name"]
        industry = client["industry"]
        project_type = random.choices(
            PROJECT_TYPES,
            weights=[1.2 if year % 2 == 0 else 0.8 for _ in PROJECT_TYPES],  # Some years favor some types
        )[0]
        # Seasonality: higher project value in Q4, more projects in Q2/Q4
        month_weights = [0.08, 0.09, 0.12, 0.13, 0.10, 0.08, 0.07, 0.07, 0.09, 0.10, 0.12, 0.13]
        project_month = random.choices(range(1, 13), weights=month_weights)[0]
        # Correlation: high value projects more likely in certain industries
        base_value = random.uniform(50000, 2000000)
        if industry in ["Banking", "Energy", "Pharma"]:
            base_value *= 1.2
        if project_type in ["Digital Transformation", "ERP Implementation"]:
            base_value *= 1.15
        # Anomaly: rare huge deal
        if random.random() < 0.02:
            base_value *= random.uniform(2, 4)
        project_value = round(base_value, 2)
        # Billable hours correlated with value
        billable_hours = int(project_value // random.uniform(200, 600))
        # Satisfaction: lower if billable hours are high
        satisfaction = max(6, min(10, int(10 - (billable_hours / 5000) * 4 + random.uniform(-1, 1))))
        # Churn: more likely if satisfaction is low or project value is low
        churn_prob = 0.1
        if satisfaction < 7:
            churn_prob += 0.15
        if project_value < 100000:
            churn_prob += 0.1
        churned = random.random() < churn_prob
        # Cross-dataset: simulate HR churn impact (e.g., more churn in CRM if year is after a high HR churn year)
        if year > 2021 and random.random() < 0.05:
            churned = True
        data.append({
            "client_id": client_id,
            "client_name": client_name,
            "industry": industry,
            "project_type": project_type,
            "project_value": project_value,
            "billable_hours": billable_hours,
            "satisfaction": satisfaction,
            "churned": churned,
            "project_month": project_month
        })
    return data

def save_crm_data(year, data, base_dir="data/companies/our_company/synthetic_internal/crm_data"):
    os.makedirs(f"{base_dir}/{year}", exist_ok=True)
    with open(f"{base_dir}/{year}/crm_data.json", "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    # Example clients list for testing
    clients = [
        {"client_id": f"C{i:03d}", "name": name, "industry": random.choice(INDUSTRIES)}
        for i, name in enumerate(CONSULTING_CLIENTS)
    ]
    for year in range(2021, 2025):
        data = generate_synthetic_crm_data(year, clients)
        save_crm_data(year, data)