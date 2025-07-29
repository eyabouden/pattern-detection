import os
import numpy as np
import json

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def clean_data(records, key_types=None, outlier_std=3, flag_only=False):
    """
    Cleans a list of dict records:
    - Fills missing values (with median/most common or None)
    - Removes exact duplicates
    - Flags or removes outliers (z-score based for numeric fields)
    - Normalizes types if key_types is provided
    - If flag_only=True, does not remove outliers but adds a '_flagged' key
    Returns cleaned records (and optionally flagged records).
    """
    if not records:
        return records
    # Remove exact duplicates
    import json
    seen = set()
    unique_records = []
    for rec in records:
        h = json.dumps(rec, sort_keys=True)
        if h not in seen:
            unique_records.append(rec)
            seen.add(h)
    records = unique_records
    # Fill missing values
    keys = records[0].keys()
    for key in keys:
        values = [rec[key] for rec in records if rec[key] is not None]
        if not values:
            continue
        if isinstance(values[0], (int, float)):
            fill_value = float(np.median(values))
        else:
            # Try to use most common value, fallback to string representation for unhashable types
            try:
                fill_value = max(set(values), key=values.count)
            except TypeError:
                # Unhashable types: use the most common string representation
                str_values = [str(v) for v in values]
                fill_value = max(set(str_values), key=str_values.count)
                # When filling, convert back to original type if possible, else use string
                for rec in records:
                    if rec[key] is None:
                        rec[key] = fill_value
                continue
        for rec in records:
            if rec[key] is None:
                rec[key] = fill_value
    # Normalize types
    if key_types:
        for rec in records:
            for k, t in key_types.items():
                try:
                    rec[k] = t(rec[k])
                except Exception:
                    pass
    # Outlier detection (z-score based, per numeric field)
    flagged = []
    for key in keys:
        values = [rec[key] for rec in records if isinstance(rec[key], (int, float))]
        if len(values) < 5:
            continue
        mean = np.mean(values)
        std = np.std(values)
        for rec in records:
            v = rec.get(key)
            if isinstance(v, (int, float)) and std > 0:
                z = abs((v - mean) / std)
                if z > outlier_std:
                    if flag_only:
                        rec.setdefault('_flagged', []).append(f'outlier_{key}')
                        flagged.append(rec)
                    else:
                        rec[key] = None  # or remove record, but we keep for pattern detection
    return records

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == '__main__':
    import os
    BASE_PATH = 'data/companies/our_company/synthetic_internal'
    YEAR = 2023  # Change as needed
    os.makedirs(f'{BASE_PATH}/crm_data/cleaned/{YEAR}', exist_ok=True)
    os.makedirs(f'{BASE_PATH}/erp_data/cleaned/{YEAR}', exist_ok=True)
    os.makedirs(f'{BASE_PATH}/financial_data/cleaned/{YEAR}', exist_ok=True)
    os.makedirs(f'{BASE_PATH}/hr_data/cleaned/{YEAR}', exist_ok=True)
    os.makedirs(f'{BASE_PATH}/project_data/cleaned/{YEAR}', exist_ok=True)
    os.makedirs(f'{BASE_PATH}/call_for_tenders/cleaned/{YEAR}', exist_ok=True)

    # CRM
    crm_path = f'{BASE_PATH}/crm_data/{YEAR}/crm_data.json'
    if os.path.exists(crm_path):
        crm_data = load_json(crm_path)
        key_types = {"project_value": float, "billable_hours": int, "satisfaction": int, "churned": bool, "project_month": int}
        cleaned = clean_data(crm_data, key_types=key_types, flag_only=True)
        save_json(f'{BASE_PATH}/crm_data/cleaned/{YEAR}/crm_data_cleaned.json', cleaned)

    # ERP
    erp_path = f'{BASE_PATH}/erp_data/{YEAR}/erp_data.json'
    if os.path.exists(erp_path):
        erp_data = load_json(erp_path)
        key_types = {"cost": float, "duration_months": int, "project_month": int}
        cleaned = clean_data(erp_data, key_types=key_types, flag_only=True)
        save_json(f'{BASE_PATH}/erp_data/cleaned/{YEAR}/erp_data_cleaned.json', cleaned)

    # Financial
    fin_path = f'{BASE_PATH}/financial_data/{YEAR}/financial_data.json'
    if os.path.exists(fin_path):
        fin_data = load_json(fin_path)
        key_types = {"revenue": float, "expenses": float, "billable_hours": int, "project_margin": float, "profit": float, "month": int}
        cleaned = clean_data(fin_data, key_types=key_types, flag_only=True)
        save_json(f'{BASE_PATH}/financial_data/cleaned/{YEAR}/financial_data_cleaned.json', cleaned)

    # HR
    hr_path = f'{BASE_PATH}/hr_data/{YEAR}/hr_data.json'
    if os.path.exists(hr_path):
        hr_data = load_json(hr_path)
        key_types = {"age": int, "years_at_company": int, "billable_hours": int, "performance_score": int, "left_company": bool, "hire_month": int}
        cleaned = clean_data(hr_data, key_types=key_types, flag_only=True)
        save_json(f'{BASE_PATH}/hr_data/cleaned/{YEAR}/hr_data_cleaned.json', cleaned)

    # Project
    proj_path = f'{BASE_PATH}/project_data/{YEAR}/project_data.json'
    if os.path.exists(proj_path):
        proj_data = load_json(proj_path)
        key_types = {"revenue": float, "profit": float, "profit_margin": float, "duration_months": int, "sales_month": int, "team_size": int}
        cleaned = clean_data(proj_data, key_types=key_types, flag_only=True)
        save_json(f'{BASE_PATH}/project_data/cleaned/{YEAR}/project_data_cleaned.json', cleaned)

    # Call for Tenders
    tenders_path = f'{BASE_PATH}/call_for_tenders/{YEAR}/call_for_tenders.json'
    if os.path.exists(tenders_path):
        tenders_data = load_json(tenders_path)
        key_types = {"estimated_value": float, "tender_month": int}
        cleaned = clean_data(tenders_data, key_types=key_types, flag_only=True)
        save_json(f'{BASE_PATH}/call_for_tenders/cleaned/{YEAR}/call_for_tenders_cleaned.json', cleaned)
    # Tender Responses (optional)
    responses_path = f'{BASE_PATH}/call_for_tenders/{YEAR}/tender_responses.json'
    if os.path.exists(responses_path):
        responses_data = load_json(responses_path)
        key_types = {"bid_amount": float}
        cleaned = clean_data(responses_data, key_types=key_types, flag_only=True)
        save_json(f'{BASE_PATH}/call_for_tenders/cleaned/{YEAR}/tender_responses_cleaned.json', cleaned) 