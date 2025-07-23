import random
import json
import os

CLIENTS = [
    "BNP Paribas", "AXA", "EDF", "SNCF", "Orange", "L'Oréal", "Renault", "TotalEnergies",
    "Société Générale", "Airbus", "Sanofi", "Carrefour", "Veolia", "ENGIE", "La Poste"
]


def generate_synthetic_financial_data(year, num_entries=12):
    data = []
    for month in range(1, num_entries+1):
        entry = {
            "month": month,
            "year": year,
            "client": random.choice(CLIENTS),
            "revenue": round(random.uniform(200000, 2000000), 2),
            "expenses": round(random.uniform(100000, 1500000), 2),
            "billable_hours": random.randint(500, 8000),
            "project_margin": round(random.uniform(0.1, 0.45), 2),
            "profit": 0.0
        }
        entry["profit"] = round(entry["revenue"] - entry["expenses"], 2)
        data.append(entry)
    return data

def save_financial_data(year, data, base_dir="data/companies/our_company/synthetic_internal/financial_data"):
    os.makedirs(f"{base_dir}/{year}", exist_ok=True)
    with open(f"{base_dir}/{year}/financial_data.json", "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    for year in range(2021, 2025):
        data = generate_synthetic_financial_data(year)
        save_financial_data(year, data) 