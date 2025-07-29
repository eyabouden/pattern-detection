import os
import json
import numpy as np
from collections import Counter, defaultdict

def load_all_years_data(base_path, dataset, years, filename):
    all_records = []
    for year in years:
        path = f"{base_path}/{dataset}/{year}/{filename}"
        if os.path.exists(path):
            with open(path, 'r') as f:
                try:
                    records = json.load(f)
                    all_records.extend(records)
                except Exception as e:
                    print(f"Error loading {path}: {e}")
    return all_records

def load_cleaned_data(base_path, dataset, year):
    path = f"{base_path}/{dataset}/cleaned/{year}/{dataset}_cleaned.json"
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return []

def detect_outliers(records, numeric_keys, outlier_std=3):
    outliers = defaultdict(list)
    for key in numeric_keys:
        values = [rec[key] for rec in records if isinstance(rec.get(key), (int, float))]
        if len(values) < 5:
            continue
        mean = np.mean(values)
        std = np.std(values)
        for rec in records:
            v = rec.get(key)
            if isinstance(v, (int, float)) and std > 0:
                z = abs((v - mean) / std)
                if z > outlier_std:
                    outliers[key].append(rec)
    return outliers

def detect_seasonality(records, month_key):
    months = [rec[month_key] for rec in records if month_key in rec]
    if not months:
        return None
    counts = Counter(months)
    most_common = counts.most_common(3)
    return most_common

def detect_correlation(records, key1, key2):
    vals1 = [rec[key1] for rec in records if isinstance(rec.get(key1), (int, float)) and isinstance(rec.get(key2), (int, float))]
    vals2 = [rec[key2] for rec in records if isinstance(rec.get(key1), (int, float)) and isinstance(rec.get(key2), (int, float))]
    if len(vals1) < 5:
        return None
    corr = np.corrcoef(vals1, vals2)[0, 1]
    return corr

def detect_at_risk_projects(projects):
    # Scenario: At-risk project if:
    # - Involves a junior consultant (<2 years experience)
    # - Multi-site (more than one location)
    # - Planned duration < 6 weeks
    # Consequences: lower margin, more delays, more complaints
    at_risk = []
    for proj in projects:
        # Assume 'team_roles' contains dicts with 'role' and 'years_experience', or fallback to 'years_at_company' if available
        junior = False
        if 'team_roles' in proj and isinstance(proj['team_roles'], list):
            for member in proj['team_roles']:
                if isinstance(member, dict) and member.get('years_experience', 3) < 2:
                    junior = True
                # Fallback: if only string roles, skip
        # Multi-site: locations is a list or int > 1
        multi_site = False
        if 'locations' in proj:
            if isinstance(proj['locations'], list) and len(proj['locations']) > 1:
                multi_site = True
            elif isinstance(proj['locations'], int) and proj['locations'] > 1:
                multi_site = True
        # Duration
        short_duration = proj.get('duration_months', 999) < 1.5  # 6 weeks = 1.5 months
        if junior and multi_site and short_duration:
            at_risk.append(proj)
    if not at_risk:
        return None
    # Consequences
    all_margins = [p.get('profit_margin', 0.0) for p in projects if isinstance(p.get('profit_margin'), (int, float))]
    avg_margin = np.mean(all_margins) if all_margins else 0.0
    risk_margins = [p.get('profit_margin', 0.0) for p in at_risk if isinstance(p.get('profit_margin'), (int, float))]
    avg_risk_margin = np.mean(risk_margins) if risk_margins else 0.0
    margin_drop = (avg_margin - avg_risk_margin) / avg_margin if avg_margin else 0.0
    # Delay rate
    all_delays = [p.get('status', '').lower() == 'delayed' for p in projects]
    risk_delays = [p.get('status', '').lower() == 'delayed' for p in at_risk]
    delay_rate = np.mean(all_delays) if all_delays else 0.0
    risk_delay_rate = np.mean(risk_delays) if risk_delays else 0.0
    # Complaints
    all_complaints = [p.get('client_complaints', 0) for p in projects]
    risk_complaints = [p.get('client_complaints', 0) for p in at_risk]
    avg_complaints = np.mean(all_complaints) if all_complaints else 0.0
    avg_risk_complaints = np.mean(risk_complaints) if risk_complaints else 0.0
    # Output scenario report
    print("\nScénario : Un projet est considéré à risque si :")
    print("– Il implique un consultant junior (< 2 ans d’expérience)")
    print("– Le contexte est multi-sites (plus d’un lieu d’intervention)")
    print("– La durée prévue est inférieure à 6 semaines")
    print("Conséquences constatées :")
    print(f"– Marge moyenne {'{:.1f}'.format(100*margin_drop) if margin_drop>0 else ''}% inférieure à la moyenne ({avg_risk_margin:.2f} vs {avg_margin:.2f})")
    print(f"– Taux de retard {'{:.1f}'.format(risk_delay_rate/delay_rate) if delay_rate>0 else ''}x la moyenne ({risk_delay_rate:.2%} vs {delay_rate:.2%})")
    print(f"– Réclamations client moyennes : {avg_risk_complaints:.2f} vs {avg_complaints:.2f}")
    print("Attendu : L’outil signale toute configuration similaire afin de permettre une anticipation ou une révision de l’approche commerciale et opérationnelle.")
    print(f"Nombre de projets à risque détectés : {len(at_risk)}")
    # Optionally, print details of at-risk projects
    for i, proj in enumerate(at_risk[:5]):
        print(f"  - Projet {proj.get('project_id', i+1)} | Marge: {proj.get('profit_margin', 'N/A')} | Statut: {proj.get('status', 'N/A')}")
    if len(at_risk) > 5:
        print(f"  ...et {len(at_risk)-5} autres.")

def main():
    BASE_PATH = 'data/companies/our_company/synthetic_internal'
    YEARS = [2021, 2022, 2023, 2024]
    datasets = [
        ('crm_data', ["project_value", "billable_hours", "satisfaction"], "project_month", 'crm_data.json'),
        ('erp_data', ["cost", "duration_months"], "project_month", 'erp_data.json'),
        ('financial_data', ["revenue", "expenses", "billable_hours", "profit"], "month", 'financial_data.json'),
        ('hr_data', ["age", "years_at_company", "billable_hours", "performance_score"], "hire_month", 'hr_data.json'),
        ('project_data', ["revenue", "profit", "profit_margin", "duration_months", "team_size"], "sales_month", 'project_data.json'),
        ('call_for_tenders', ["estimated_value"], "tender_month", 'call_for_tenders.json'),
    ]
    print(f"Pattern Detection Report for ALL YEARS ({YEARS[0]}–{YEARS[-1]})\n{'='*50}")
    all_data = {}
    for dataset, numeric_keys, month_key, filename in datasets:
        records = load_all_years_data(BASE_PATH, dataset, YEARS, filename)
        all_data[dataset] = records
        print(f"\n--- {dataset.upper()} ---")
        print(f"Loaded {len(records)} records from {YEARS[0]}–{YEARS[-1]}.")
        # Outlier detection
        outliers = detect_outliers(records, numeric_keys)
        for key, recs in outliers.items():
            print(f"  Outliers in {key}: {len(recs)} records flagged.")
        # Seasonality
        seasonality = detect_seasonality(records, month_key)
        if seasonality:
            print(f"  Most active months ({month_key}): {seasonality}")
        # Example correlation (first two numeric keys)
        if len(numeric_keys) >= 2:
            corr = detect_correlation(records, numeric_keys[0], numeric_keys[1])
            if corr is not None:
                print(f"  Correlation between {numeric_keys[0]} and {numeric_keys[1]}: {corr:.2f}")
        # Flagged records
        flagged = [rec for rec in records if '_flagged' in rec]
        if flagged:
            print(f"  {len(flagged)} records flagged as suspicious/anomalous.")
        # TODO: Add more advanced pattern detection (trends, clustering, etc.)
    # Scenario-based pattern detection for project_data
    if 'project_data' in all_data:
        detect_at_risk_projects(all_data['project_data'])
    # TODO: Cross-dataset pattern detection (e.g., HR churn vs. sales drop)
    print("\n[TODO] Cross-dataset pattern detection and deeper analytics.")

if __name__ == "__main__":
    main() 