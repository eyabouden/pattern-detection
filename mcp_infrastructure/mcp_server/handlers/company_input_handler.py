from agents.company_setup_agents.company_identifier_agent import identify_company

def handle_company_input(company_name: str) -> dict:
    return identify_company(company_name) 