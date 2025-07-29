import random
import json
import os

CLIENTS = [
    "BNP Paribas", "AXA", "EDF", "SNCF", "Orange", "L'Oréal", "Renault", "TotalEnergies",
    "Société Générale", "Airbus", "Sanofi", "Carrefour", "Veolia", "ENGIE", "La Poste"
]


def generate_synthetic_financial_data(year, clients, num_entries=12):
    data = []
    client_ids = [client["client_id"] for client in clients]
    for month in range(1, num_entries+1):
        # Seasonality: higher revenue in Q2/Q4, higher expenses in Q1
        revenue_base = random.uniform(200000, 2000000)
        if month in [4,5,6,10,11,12]:
            revenue_base *= 1.15
        expenses_base = random.uniform(100000, 1500000)
        if month in [1,2,3]:
            expenses_base *= 1.2
        # Correlation: higher billable hours → higher revenue
        billable_hours = random.randint(500, 8000)
        revenue = revenue_base + billable_hours * random.uniform(10, 30)
        # Margin: lower if expenses are high
        project_margin = round(random.uniform(0.1, 0.45) - (expenses_base / 20000000), 2)
        # Anomaly: rare negative profit
        profit = revenue - expenses_base
        if random.random() < 0.02:
            profit = -abs(profit) * random.uniform(1, 2)
        # Cross-dataset: simulate impact of project loss (e.g., lower revenue after a bad project)
        if year > 2021 and random.random() < 0.05:
            revenue *= 0.7
            profit *= 0.5
        entry = {
            "month": month,
            "year": year,
            "client_id": random.choice(client_ids),
            "revenue": round(revenue, 2),
            "expenses": round(expenses_base, 2),
            "billable_hours": billable_hours,
            "project_margin": project_margin,
            "profit": round(profit, 2)
        }
        data.append(entry)
    return data

def save_financial_data(year, data, base_dir="data/companies/our_company/synthetic_internal/financial_data"):
    os.makedirs(f"{base_dir}/{year}", exist_ok=True)
    with open(f"{base_dir}/{year}/financial_data.json", "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    # Example clients list for testing
    clients = [
        {"client_id": f"C{i:03d}", "name": name, "industry": ""}
        for i, name in enumerate(CLIENTS)
    ]
    for year in range(2021, 2025):
        data = generate_synthetic_financial_data(year, clients)
        save_financial_data(year, data) 