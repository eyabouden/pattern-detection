import json
import random
import os

# Define possible values for enrichment
INDUSTRIES = [
    "Banking", "Insurance", "Energy", "Public Sector", "Telecom", "Retail", "Pharma", "Transport"
]
TEAM_SIZES = [3, 4, 5, 6, 7, 8, 9, 10]

# Margin as a percentage (simulate realistic consulting margins)
MARGIN_RANGE = {
    "low": (5, 12),
    "medium": (13, 22),
    "high": (23, 35)
}

# Load existing tenders
def enrich_tenders(input_path, output_path):
    with open(input_path, 'r') as f:
        tenders = json.load(f)

    enriched = []
    for tender in tenders:
        # Assign industry randomly
        industry = random.choice(INDUSTRIES)
        # Assign team size based on estimated value
        if tender["estimated_value"] < 500000:
            team_size = random.choice(TEAM_SIZES[:3])
        elif tender["estimated_value"] < 2000000:
            team_size = random.choice(TEAM_SIZES[2:5])
        else:
            team_size = random.choice(TEAM_SIZES[4:])
        # Assign margin based on status and randomness
        if tender["status"] == "Awarded":
            margin_pct = random.uniform(*MARGIN_RANGE["medium"])
        else:
            margin_pct = random.uniform(*MARGIN_RANGE["low"])
        tender["industry"] = industry
        tender["team_size"] = team_size
        tender["margin_pct"] = round(margin_pct, 2)
        enriched.append(tender)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(enriched, f, indent=2)

if __name__ == "__main__":
    base_dir = "data/companies/our_company/synthetic_internal/call_for_tenders"
    years = ["2021", "2022", "2023", "2024"]
    for year in years:
        input_path = f"{base_dir}/{year}/call_for_tenders.json"
        output_path = f"{base_dir}/{year}/call_for_tenders_enriched.json"
        if os.path.exists(input_path):
            print(f"Enriching {input_path} ...")
            enrich_tenders(input_path, output_path)
        else:
            print(f"File not found: {input_path}")
