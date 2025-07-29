from fastapi import APIRouter, Query
from pydantic import BaseModel
import pandas as pd
import os
import json
from agents.pattern_detection_agents.decision_tree_pattern_agent import DecisionTreePatternAgent

router = APIRouter()

class PatternDetectionRequest(BaseModel):
    data_type: str = Query(..., description="Type de données à analyser: 'project', 'crm', 'tender'")
    target_col: str = Query(..., description="Colonne cible à prédire")
    year: int = Query(2021, description="Année des données à charger")

@router.post("/detect-patterns")
def detect_patterns(request: PatternDetectionRequest):
    # Map data_type to file path
    data_paths = {
        'project': f"data/companies/our_company/synthetic_internal/project_data/{request.year}/project_data.json",
        'crm': f"data/companies/our_company/synthetic_internal/crm_data/{request.year}/crm_data.json",
        'tender': f"data/companies/our_company/synthetic_internal/call_for_tenders/{request.year}/call_for_tenders.json"
    }
    if request.data_type not in data_paths:
        return {"error": "Invalid data_type. Choose from 'project', 'crm', 'tender'."}
    data_path = data_paths[request.data_type]
    if not os.path.exists(data_path):
        return {"error": f"Data file not found: {data_path}"}
    with open(data_path, 'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    agent = DecisionTreePatternAgent()
    result = agent.extract_patterns(df, request.target_col)
    return result 