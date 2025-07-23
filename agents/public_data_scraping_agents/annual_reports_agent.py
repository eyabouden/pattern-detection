from utils.web_scraping_utils import search_annual_report_pdfs, download_pdfs, extract_text_from_pdfs
from utils.data_utils import ensure_dir

def process_annual_reports(company_name: str, base_data_dir: str = "data/companies"):
    # Prepare directories
    pdf_dir = f"{base_data_dir}/{company_name}/public_data/annual_reports/pdfs"
    extracted_dir = f"{base_data_dir}/{company_name}/public_data/annual_reports/extracted"
    ensure_dir(pdf_dir)
    ensure_dir(extracted_dir)

    # 1. Search for annual report PDFs
    pdf_links = search_annual_report_pdfs(company_name)
    if not pdf_links:
        print(f"No annual report PDFs found for {company_name}")
        return

    # 2. Download PDFs
    download_pdfs(pdf_links, pdf_dir)

    # 3. Extract text from PDFs
    extract_text_from_pdfs(pdf_dir, extracted_dir)
    print(f"Annual reports processed for {company_name}") 