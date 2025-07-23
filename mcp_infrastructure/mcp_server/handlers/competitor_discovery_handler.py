from agents.company_setup_agents.competitor_discovery_agent import find_competitors
from config.settings import COMPETITOR_COUNT

def handle_competitor_discovery(company_name: str) -> dict:
    """
    Handle the competitor discovery process and return detailed results.
    """
    competitor_details = find_competitors(company_name, COMPETITOR_COUNT)
    
    # Format the response
    response = {
        "company_name": company_name,
        "competitors": [
            {
                "name": comp["name"],
                "confidence_score": comp["confidence_score"],
                "source": comp["source"],
                "industry_match": comp["industry_match"]
            }
            for comp in competitor_details
        ],
        "total_found": len(competitor_details)
    }
    
    return response 