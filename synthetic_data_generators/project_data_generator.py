import random
import json
import os
from datetime import datetime, timedelta

PROJECT_TYPES = [
    "Digital Transformation", "ERP Implementation", "Data Analytics", "Cloud Migration",
    "Cybersecurity Audit", "Process Optimization", "AI/ML Deployment", "IT Outsourcing"
]
INDUSTRIES = [
    "Banking", "Insurance", "Energy", "Public Sector", "Telecom", "Retail", "Pharma", "Transport"
]
CLIENTS = [
    "BNP Paribas", "AXA", "EDF", "SNCF", "Orange", "L'Oréal", "Renault", "TotalEnergies",
    "Société Générale", "Airbus", "Sanofi", "Carrefour", "Veolia", "ENGIE", "La Poste"
]
TEAM_ROLES = [
    "Consultant", "Senior Consultant", "Manager", "Data Scientist", "Cloud Architect",
    "Business Analyst", "Project Manager"
]

def random_date(year, seasonality=True):
    # Simulate seasonality: more projects start in March-June and September-November
    if seasonality:
        month_weights = [0.05, 0.07, 0.12, 0.13, 0.13, 0.10, 0.06, 0.05, 0.10, 0.09, 0.07, 0.03]
        month = random.choices(range(1, 13), weights=month_weights)[0]
    else:
        month = random.randint(1, 12)
    day = random.randint(1, 28)
    return datetime(year, month, day)

def generate_synthetic_project_data(year, num_projects=60):
    data = []
    client_repeat_prob = {client: random.uniform(0.2, 0.7) for client in CLIENTS}
    client_last_project = {}

    for i in range(num_projects):
        client = random.choice(CLIENTS)
        is_repeat = client in client_last_project and random.random() < client_repeat_prob[client]
        industry = random.choice(INDUSTRIES)
        project_type = random.choices(
            PROJECT_TYPES,
            weights=[1.2, 1.1, 1.0, 1.0, 0.8, 0.9, 1.1, 0.7],  # Some types more common
        )[0]
        start_date = random_date(year)
        duration_months = random.choices([3, 6, 9, 12, 15], weights=[0.2, 0.4, 0.2, 0.15, 0.05])[0]
        end_date = start_date + timedelta(days=duration_months * 30)
        complexity = random.choices(["Low", "Medium", "High"], weights=[0.3, 0.5, 0.2])[0]
        team_size = random.randint(3, 12)
        team = random.choices(TEAM_ROLES, k=team_size)
        base_revenue = random.uniform(100000, 2000000)
        # Revenue is higher for certain project types and industries
        if project_type in ["Digital Transformation", "ERP Implementation"]:
            base_revenue *= 1.2
        if industry in ["Banking", "Energy", "Pharma"]:
            base_revenue *= 1.15
        # Profit is correlated with duration and complexity
        profit_margin = random.uniform(0.18, 0.35)
        if complexity == "High":
            profit_margin -= 0.05
        profit = base_revenue * profit_margin
        # Seasonality: more sales in certain months
        sales_month = start_date.month
        # Save for repeat client logic
        client_last_project[client] = end_date

        project = {
            "project_id": f"P{year}{i:04d}",
            "client": client,
            "industry": industry,
            "is_repeat_client": is_repeat,
            "project_type": project_type,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "duration_months": duration_months,
            "sales_month": sales_month,
            "complexity": complexity,
            "team_size": team_size,
            "team_roles": team,
            "revenue": round(base_revenue, 2),
            "profit": round(profit, 2),
            "profit_margin": round(profit_margin, 2)
        }
        data.append(project)
    return data

def generate_synthetic_call_for_tenders(year, num_tenders=40):
    TENDER_TYPES = [
        "IT Services", "Construction", "Consulting", "Maintenance", "Supply Chain", "Marketing"
    ]
    TENDER_STATUSES = ["Open", "Closed", "Awarded", "Cancelled"]
    CLIENT_SIZES = ["TPE", "PME", "ETI", "Grand Compte"]
    COMMUNICATION_CHANNELS = ["LinkedIn", "Email", "Phone", "Website", "Referral"]
    data = []
    for i in range(num_tenders):
        tender_id = f"T{year}{i:04d}"
        tender_type = random.choice(TENDER_TYPES)
        issue_date = random_date(year)
        closing_date = issue_date + timedelta(days=random.randint(15, 60))
        status = random.choices(TENDER_STATUSES, weights=[0.4, 0.3, 0.25, 0.05])[0]
        client_size = random.choice(CLIENT_SIZES)
        communication_channel = random.choice(COMMUNICATION_CHANNELS)
        description = f"{tender_type} tender for project {i}"
        estimated_value = random.uniform(50000, 5000000)
        data.append({
            "tender_id": tender_id,
            "tender_type": tender_type,
            "issue_date": issue_date.strftime("%Y-%m-%d"),
            "closing_date": closing_date.strftime("%Y-%m-%d"),
            "status": status,
            "client_size": client_size,
            "communication_channel": communication_channel,
            "description": description,
            "estimated_value": round(estimated_value, 2)
        })
    return data

def generate_synthetic_tender_responses(tenders, num_responses_per_tender=3):
    RESPONDERS = [
        "Company A", "Company B", "Company C", "Company D", "Company E"
    ]
    data = []
    for tender in tenders:
        tender_id = tender["tender_id"]
        for i in range(num_responses_per_tender):
            responder = random.choice(RESPONDERS)
            response_date = datetime.strptime(tender["issue_date"], "%Y-%m-%d") + timedelta(days=random.randint(1, 30))
            bid_amount = tender["estimated_value"] * random.uniform(0.8, 1.2)
            status = random.choices(["Submitted", "Rejected", "Accepted"], weights=[0.7, 0.2, 0.1])[0]
            data.append({
                "tender_id": tender_id,
                "responder": responder,
                "response_date": response_date.strftime("%Y-%m-%d"),
                "bid_amount": round(bid_amount, 2),
                "status": status
            })
    return data

def save_call_for_tenders_data(year, tenders, responses, base_dir="data/companies/our_company/synthetic_internal/call_for_tenders"):
    os.makedirs(f"{base_dir}/{year}", exist_ok=True)
    with open(f"{base_dir}/{year}/call_for_tenders.json", "w") as f:
        json.dump(tenders, f, indent=2)
    with open(f"{base_dir}/{year}/tender_responses.json", "w") as f:
        json.dump(responses, f, indent=2)

def save_project_data(year, data, base_dir="data/companies/our_company/synthetic_internal/project_data"):
    os.makedirs(f"{base_dir}/{year}", exist_ok=True)
    with open(f"{base_dir}/{year}/project_data.json", "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    for year in range(2021, 2025):
        project_data = generate_synthetic_project_data(year)
        save_project_data(year, project_data)
        tenders = generate_synthetic_call_for_tenders(year)
        responses = generate_synthetic_tender_responses(tenders)
        save_call_for_tenders_data(year, tenders, responses)
