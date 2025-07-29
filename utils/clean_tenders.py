import os
import json
import pandas as pd

def clean_tenders(input_path, output_path):
    # Load data
    with open(input_path, 'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)

    # 1. Remove duplicates
    df = df.drop_duplicates(subset=["tender_id"])

    # 2. Remove rows with missing critical fields
    critical_fields = ["tender_id", "tender_type", "industry", "team_size", "margin_pct", "estimated_value", "status"]
    df = df.dropna(subset=critical_fields)

    # 3. Remove negative or zero values for team_size, margin, estimated_value
    df = df[(df["team_size"] > 0) & (df["margin_pct"] >= 0) & (df["estimated_value"] > 0)]

    # 4. Standardize text fields (strip, lower, title case for display)
    df["tender_type"] = df["tender_type"].str.strip().str.title()
    df["industry"] = df["industry"].str.strip().str.title()
    df["status"] = df["status"].str.strip().str.title()
    df["client_size"] = df["client_size"].str.strip().str.title()

    # 5. (Optional) Convert dates to datetime
    if "issue_date" in df.columns:
        df["issue_date"] = pd.to_datetime(df["issue_date"], errors="coerce")
    if "closing_date" in df.columns:
        df["closing_date"] = pd.to_datetime(df["closing_date"], errors="coerce")

    # 6. Remove rows with invalid dates
    if "issue_date" in df.columns and "closing_date" in df.columns:
        df = df[df["issue_date"].notna() & df["closing_date"].notna()]

    # Save cleaned data
    df = df.reset_index(drop=True)
    df.to_json(output_path, orient="records", indent=2, date_format="iso")

if __name__ == "__main__":
    # Example for 2024, adapt for all years as needed
    input_path = "data/companies/our_company/synthetic_internal/call_for_tenders/2024/call_for_tenders_enriched.json"
    output_path = "data/companies/our_company/synthetic_internal/call_for_tenders/2024/call_for_tenders_cleaned.json"
    clean_tenders(input_path, output_path)
