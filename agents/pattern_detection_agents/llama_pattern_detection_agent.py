import os
import json
from llama_cpp import Llama

MODEL_PATH = "llama-2-7b-chat.Q4_K_M.gguf"  # <-- Set your model path here

# Load the Llama model (adjust n_ctx and n_threads as needed for your hardware)
llm = Llama(model_path=MODEL_PATH, n_ctx=2048, n_threads=4)

BASE_PATH = 'data/companies/our_company/synthetic_internal'
YEARS = [2021, 2022, 2023, 2024]


def load_all_years_data(base_path, dataset, years, filename):
    all_records = []
    for year in years:
        path = f"{base_path}/{dataset}/{year}/{filename}"
        if os.path.exists(path):
            with open(path, 'r') as f:
                try:
                    records = json.load(f)
                    all_records.extend(records)
                except Exception as e:
                    print(f"Error loading {path}: {e}")
    return all_records

def llm_pattern_analysis(records, prompt_template, sample_size=20):
    # Sample or summarize the data for the LLM
    sample = records[:sample_size]
    prompt = prompt_template.format(sample=json.dumps(sample, ensure_ascii=False, indent=2))
    output = llm(prompt, max_tokens=512, stop=["</s>"])
    return output["choices"][0]["text"]

prompt_template = (
    "Voici un échantillon de données de projet (format JSON) :\n{sample}\n"
    "En tant qu'expert en analyse de données d'entreprise, décris tous les motifs cachés, risques, anomalies ou scénarios métier détectés dans ces données. "
    "Présente les résultats en français, dans un style de rapport d'entreprise, avec des recommandations si possible."
)

def main():
    print("Rapport d'analyse Llama sur les motifs cachés dans les données de projet (toutes années)")
    project_data = load_all_years_data(BASE_PATH, 'project_data', YEARS, 'project_data.json')
    if not project_data:
        print("Aucune donnée de projet trouvée.")
        return
    llm_report = llm_pattern_analysis(project_data, prompt_template)
    print("\n--- Rapport Llama ---\n")
    print(llm_report)

if __name__ == "__main__":
    main() 