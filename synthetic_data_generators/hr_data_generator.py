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
        employee = {
            "employee_id": f"H{year}{i:03d}",
            "role": random.choice(CONSULTING_ROLES),
            "department": random.choice(DEPARTMENTS),
            "age": random.randint(24, 60),
            "years_at_company": random.randint(0, 20),
            "billable_hours": random.randint(800, 2200),
            "performance_score": random.randint(6, 10),
            "left_company": random.choices([True, False], weights=[1, 9])[0]
        }
        data.append(employee)
    return data

def save_hr_data(year, data, base_dir="data/companies/our_company/synthetic_internal/hr_data"):
    os.makedirs(f"{base_dir}/{year}", exist_ok=True)
    with open(f"{base_dir}/{year}/hr_data.json", "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    for year in range(2021, 2025):
        data = generate_synthetic_hr_data(year)
        save_hr_data(year, data) 