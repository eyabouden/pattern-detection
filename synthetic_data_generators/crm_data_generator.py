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

def generate_synthetic_crm_data(year, num_clients=30):
    data = []
    for i in range(num_clients):
        client = {
            "client_id": f"C{year}{i:03d}",
            "client_name": random.choice(CONSULTING_CLIENTS),
            "industry": random.choice(INDUSTRIES),
            "project_type": random.choice(PROJECT_TYPES),
            "project_value": round(random.uniform(50000, 2000000), 2),
            "billable_hours": random.randint(100, 5000),
            "satisfaction": random.randint(6, 10),  # Consulting clients expect high quality
            "churned": random.choices([True, False], weights=[1, 9])[0]  # Most clients retained
        }
        data.append(client)
    return data

def save_crm_data(year, data, base_dir="data/companies/our_company/synthetic_internal/crm_data"):
    os.makedirs(f"{base_dir}/{year}", exist_ok=True)
    with open(f"{base_dir}/{year}/crm_data.json", "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    for year in range(2021, 2025):
        data = generate_synthetic_crm_data(year)
        save_crm_data(year, data)