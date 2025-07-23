from agents.orchestrator.main_workflow_orchestrator import run_workflow

if __name__ == "__main__":
    company_name = input("Enter your company name: ").strip()
    run_workflow(company_name) 