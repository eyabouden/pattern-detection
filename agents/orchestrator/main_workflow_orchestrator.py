import json
from agents.a2a_protocol.agent_registry import AgentRegistry
from agents.a2a_protocol.communication_layer import CommunicationLayer
from agents.pattern_detection_agents.churn_agent import ChurnPatternAgent
from agents.pattern_detection_agents.seasonality_agent import SeasonalityPatternAgent
from agents.pattern_detection_agents.profitability_agent import ProfitabilityPatternAgent
from agents.pattern_detection_agents.repeat_client_agent import RepeatClientPatternAgent
from agents.pattern_detection_agents.success_recipe_agent import SuccessRecipeAgent
from agents.pattern_detection_agents.erp_pattern_agent import ERPPatternAgent
from agents.pattern_detection_agents.hr_pattern_agent import HRPatternAgent
from agents.pattern_detection_agents.financial_pattern_agent import FinancialPatternAgent
from agents.a2a_protocol.message_protocol import AgentMessage

# Utility to load synthetic data
def load_jsons_from_dir(base_dir):
    import os
    all_data = []
    for year_folder in os.listdir(base_dir):
        year_path = os.path.join(base_dir, year_folder)
        for file in os.listdir(year_path):
            if file.endswith('.json'):
                with open(os.path.join(year_path, file)) as f:
                    all_data.extend(json.load(f))
    return all_data

def run_pattern_detection():
    crm_data = load_jsons_from_dir("data/companies/our_company/synthetic_internal/crm_data")
    project_data = load_jsons_from_dir("data/companies/our_company/synthetic_internal/project_data")
    erp_data = load_jsons_from_dir("data/companies/our_company/synthetic_internal/erp_data")
    hr_data = load_jsons_from_dir("data/companies/our_company/synthetic_internal/hr_data")
    financial_data = load_jsons_from_dir("data/companies/our_company/synthetic_internal/financial_data")

    registry = AgentRegistry()
    registry.register("churn_agent", ChurnPatternAgent(crm_data))
    registry.register("seasonality_agent", SeasonalityPatternAgent(project_data))
    registry.register("profitability_agent", ProfitabilityPatternAgent(project_data))
    registry.register("repeat_client_agent", RepeatClientPatternAgent(project_data))
    registry.register("success_recipe_agent", SuccessRecipeAgent(project_data))
    registry.register("erp_pattern_agent", ERPPatternAgent(erp_data))
    registry.register("hr_pattern_agent", HRPatternAgent(hr_data))
    registry.register("financial_pattern_agent", FinancialPatternAgent(financial_data))
    comms = CommunicationLayer(registry)

    # Request churn pattern
    churn_msg = AgentMessage("orchestrator", "churn_agent", "REQUEST_PATTERN")
    churn_result = comms.send(churn_msg)
    print("\nChurn Pattern:\n", churn_result.get("summary", churn_result))

    # Request seasonality pattern
    seasonality_msg = AgentMessage("orchestrator", "seasonality_agent", "REQUEST_PATTERN")
    seasonality_result = comms.send(seasonality_msg)
    print("\nSeasonality Pattern:\n", seasonality_result)

    # Request profitability pattern
    profit_msg = AgentMessage("orchestrator", "profitability_agent", "REQUEST_PATTERN")
    profit_result = comms.send(profit_msg)
    print("\nProfitability Pattern:\n", profit_result.get("summary", profit_result))

    # Request repeat client pattern
    repeat_msg = AgentMessage("orchestrator", "repeat_client_agent", "REQUEST_PATTERN")
    repeat_result = comms.send(repeat_msg)
    print("\nRepeat Client Pattern:\n", repeat_result.get("summary", repeat_result))

    # Request success recipe pattern
    success_msg = AgentMessage("orchestrator", "success_recipe_agent", "REQUEST_PATTERN")
    success_result = comms.send(success_msg)
    print("\nSuccess Recipe Patterns:\n", "\n".join(success_result.get("recipes", [])))

    # Request ERP pattern
    erp_msg = AgentMessage("orchestrator", "erp_pattern_agent", "REQUEST_PATTERN")
    erp_result = comms.send(erp_msg)
    print("\nERP Delay Rules:\n", "\n".join(erp_result.get("rules", [])))

    # Request HR pattern
    hr_msg = AgentMessage("orchestrator", "hr_pattern_agent", "REQUEST_PATTERN")
    hr_result = comms.send(hr_msg)
    print("\nHR Turnover Rules:\n", "\n".join(hr_result.get("rules", [])))

    # Request Financial pattern
    fin_msg = AgentMessage("orchestrator", "financial_pattern_agent", "REQUEST_PATTERN")
    fin_result = comms.send(fin_msg)
    print("\nFinancial Profit Rules:\n", "\n".join(fin_result.get("rules", [])))

if __name__ == "__main__":
    run_pattern_detection() 