from googlesearch import search
import os, requests, fitz, json
from tqdm import tqdm
import time

def search_annual_report_pdfs(company, max_results=5):
    query = f'"{company}" "annual report" filetype:pdf'
    pdf_links = []
    
    try:
        time.sleep(1.5)  # Rate limiting
        for url in search(query, num_results=max_results, lang="en"):
            if url.lower().endswith('.pdf'):
                pdf_links.append(url)
    except Exception as e:
        print(f"Failed to search for annual reports for {company}: {e}")
    
    return pdf_links

def download_pdfs(pdf_links, download_dir="pdfs"):
    os.makedirs(download_dir, exist_ok=True)
    for link in pdf_links:
        filename = os.path.join(download_dir, link.split("/")[-1].split("?")[0])
        if not os.path.exists(filename):
            try:
                pdf_response = requests.get(link, timeout=20)
                with open(filename, "wb") as f:
                    f.write(pdf_response.content)
            except Exception as e:
                print(f"Failed to download {link}: {e}")

def extract_text_from_pdfs(pdf_dir="pdfs", output_dir="extracted"):
    os.makedirs(output_dir, exist_ok=True)
    for pdf_file in tqdm(os.listdir(pdf_dir)):
        if not pdf_file.endswith('.pdf'):
            continue
        pdf_path = os.path.join(pdf_dir, pdf_file)
        try:
            doc = fitz.open(pdf_path)
            text = ""
            for page in doc:
                text += page.get_text()
            data = {
                "filename": pdf_file,
                "text": text
            }
            json_path = os.path.join(output_dir, pdf_file.replace('.pdf', '.json'))
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Extracted and saved: {json_path}")
        except Exception as e:
            print(f"Failed to extract {pdf_file}: {e}") 