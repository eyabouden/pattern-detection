from typing import List, Dict
from utils.competitor_discovery_utils import (
    search_competitors_web,
    search_competitors_linkedin,
    search_competitors_news,
    clean_company_name,
    validate_competitor
)

class CompetitorDiscoveryAgent:
    def __init__(self, target_count: int = 4):
        self.target_count = target_count
        self.competitors = set()

    def find_competitors(self, company_name: str) -> List[Dict]:
        """
        Find competitors using multiple sources and strategies.
        Returns list of validated competitor information.
        """
        clean_name = clean_company_name(company_name)
        
        print(f"Searching for competitors of {clean_name}...")
        
        # 1. Web Search Strategy
        print("  - Searching web sources...")
        web_competitors = search_competitors_web(clean_name)
        self._add_competitors(web_competitors)

        # 2. LinkedIn Strategy
        print("  - Searching LinkedIn data...")
        linkedin_competitors = search_competitors_linkedin(clean_name)
        self._add_competitors(linkedin_competitors)

        # 3. News/Articles Strategy
        print("  - Searching news sources...")
        news_competitors = search_competitors_news(clean_name)
        self._add_competitors(news_competitors)

        # If we don't have enough competitors, add some fallback options
        if len(self.competitors) < 2:
            print("  - Adding fallback competitors...")
            self._add_fallback_competitors(clean_name)

        # Validate and rank competitors
        print("  - Validating competitors...")
        validated_competitors = []
        for comp in self.competitors:
            if len(validated_competitors) >= self.target_count:
                break
            
            validation_result = validate_competitor(comp, clean_name)
            if validation_result["is_valid"]:
                validated_competitors.append({
                    "name": comp,
                    "confidence_score": validation_result["confidence_score"],
                    "source": validation_result["source"],
                    "industry_match": validation_result["industry_match"]
                })

        # Sort by confidence score
        validated_competitors.sort(key=lambda x: x["confidence_score"], reverse=True)
        
        # If we still don't have enough, add some basic fallbacks
        while len(validated_competitors) < self.target_count:
            fallback_name = f"Competitor_{len(validated_competitors) + 1}"
            validated_competitors.append({
                "name": fallback_name,
                "confidence_score": 0.1,
                "source": "fallback",
                "industry_match": False
            })
        
        return validated_competitors[:self.target_count]

    def _add_competitors(self, new_competitors: List[str]):
        """Add new competitors to the set, avoiding duplicates"""
        self.competitors.update(new_competitors)

    def _add_fallback_competitors(self, company_name: str):
        """Add some basic fallback competitors based on common patterns"""
        # Common consulting/tech companies that might be competitors
        fallbacks = [
            "Accenture", "Deloitte", "PwC", "EY", "KPMG",
            "IBM", "Microsoft", "Oracle", "SAP", "Salesforce",
            "Cognizant", "Infosys", "TCS", "Wipro", "HCL"
        ]
        
        # Add a few random fallbacks
        import random
        selected = random.sample(fallbacks, min(3, len(fallbacks)))
        self.competitors.update(selected)

def find_competitors(company_name: str, count: int = 4) -> List[Dict]:
    """
    Main function to find competitors for a given company.
    Returns list of competitor details.
    """
    agent = CompetitorDiscoveryAgent(target_count=count)
    return agent.find_competitors(company_name) 