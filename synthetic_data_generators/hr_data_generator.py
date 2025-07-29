import random
import json
import os

CONSULTING_ROLES = [
    "Consultant", "Senior Consultant", "Manager", "Senior Manager", "Director", "Partner",
    "Data Scientist", "Cloud Architect", "Business Analyst", "Project Manager"
]
DEPARTMENTS = ["Consulting", "Technology", "Digital", "Delivery", "Operations"]


def generate_synthetic_hr_data(year, num_employees=40):
    data = []
    for i in range(num_employees):
        employee_id = f"H{year}{i:03d}"
        role = random.choice(CONSULTING_ROLES)
        department = random.choice(DEPARTMENTS)
        # Seasonality: more hiring in Q1, more exits in Q3/Q4
        hire_month = random.choices(range(1, 13), weights=[0.15,0.13,0.10,0.08,0.07,0.06,0.05,0.05,0.07,0.08,0.10,0.11])[0]
        age = random.randint(24, 60)
        years_at_company = random.randint(0, 20)
        billable_hours = random.randint(800, 2200)
        # Correlation: low performance → higher chance of leaving
        performance_score = random.randint(6, 10)
        leave_prob = 0.1
        if performance_score < 7:
            leave_prob += 0.2
        if years_at_company < 2:
            leave_prob += 0.1
        # Anomaly: rare mass exit
        left_company = random.random() < leave_prob
        if random.random() < 0.02:
            left_company = True
        # Cross-dataset: simulate impact of financial stress (e.g., more exits after bad financial year)
        if year > 2021 and random.random() < 0.05:
            left_company = True
        data.append({
            "employee_id": employee_id,
            "role": role,
            "department": department,
            "age": age,
            "years_at_company": years_at_company,
            "billable_hours": billable_hours,
            "performance_score": performance_score,
            "left_company": left_company,
            "hire_month": hire_month
        })
    return data

def save_hr_data(year, data, base_dir="data/companies/our_company/synthetic_internal/hr_data"):
    os.makedirs(f"{base_dir}/{year}", exist_ok=True)
    with open(f"{base_dir}/{year}/hr_data.json", "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    for year in range(2021, 2025):
        data = generate_synthetic_hr_data(year)
        save_hr_data(year, data) 