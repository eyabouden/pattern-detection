from googlesearch import search
import re
from typing import List, Dict
import requests
from bs4 import BeautifulSoup
import time
import random

def clean_company_name(name: str) -> str:
    """Clean and standardize company name"""
    # Remove legal entities (Inc., Ltd., etc.)
    legal_entities = r'\s+(Inc\.|Ltd\.|LLC|Corp\.|Corporation|Limited|Company)\.?$'
    name = re.sub(legal_entities, '', name, flags=re.IGNORECASE)
    # Remove special characters and extra spaces
    name = re.sub(r'[^\w\s-]', '', name)
    return name.strip()

def safe_google_search(query: str, max_results: int = 5, delay: float = 1.0) -> List[str]:
    """Perform a safe Google search with error handling and rate limiting"""
    try:
        time.sleep(delay)  # Rate limiting
        results = []
        for url in search(query, num_results=max_results, lang="en"):
            results.append(url)
        return results
    except Exception as e:
        print(f"Google search failed for query '{query}': {e}")
        return []

def extract_company_names_from_urls(urls: List[str]) -> List[str]:
    """Extract company names from search result URLs"""
    companies = set()
    
    for url in urls:
        try:
            # Extract domain name and look for company patterns
            domain = url.split('/')[2] if len(url.split('/')) > 2 else url
            
            # Remove common domain suffixes
            domain = re.sub(r'\.(com|org|net|co|uk|fr|de|it|es)$', '', domain, flags=re.IGNORECASE)
            
            # Split by dots and look for potential company names
            parts = domain.split('.')
            for part in parts:
                if len(part) > 2 and part[0].isupper():
                    companies.add(part)
                    
        except Exception as e:
            continue
    
    return list(companies)

def search_competitors_web(company_name: str) -> List[str]:
    """Find competitors using web search"""
    competitors = set()
    
    # Strategy 1: Direct competitor search
    query = f'"{company_name}" competitors'
    urls = safe_google_search(query, max_results=5, delay=1.5)
    
    # Extract company names from URLs
    url_companies = extract_company_names_from_urls(urls)
    competitors.update(url_companies)
    
    # Strategy 2: Industry-specific search
    query = f'"{company_name}" industry leaders market share'
    urls = safe_google_search(query, max_results=3, delay=2.0)
    
    url_companies = extract_company_names_from_urls(urls)
    competitors.update(url_companies)
    
    # Strategy 3: "competes with" search
    query = f'"{company_name}" competes with'
    urls = safe_google_search(query, max_results=3, delay=2.0)
    
    url_companies = extract_company_names_from_urls(urls)
    competitors.update(url_companies)

    return list(competitors)

def search_competitors_linkedin(company_name: str) -> List[str]:
    """Find competitors using LinkedIn data"""
    competitors = set()
    
    # Search for LinkedIn company pages
    query = f'site:linkedin.com "{company_name}" "similar companies"'
    urls = safe_google_search(query, max_results=3, delay=2.0)
    
    # Extract company names from LinkedIn URLs
    for url in urls:
        if 'linkedin.com/company/' in url:
            # Extract company name from LinkedIn URL
            parts = url.split('/')
            for i, part in enumerate(parts):
                if part == 'company' and i + 1 < len(parts):
                    company_part = parts[i + 1]
                    if company_part and len(company_part) > 2:
                        competitors.add(company_part.replace('-', ' ').title())
    
    return list(competitors)

def search_competitors_news(company_name: str) -> List[str]:
    """Find competitors from recent news articles"""
    competitors = set()
    
    query = f'"{company_name}" market competition news'
    urls = safe_google_search(query, max_results=3, delay=2.0)
    
    # Extract company names from news URLs
    url_companies = extract_company_names_from_urls(urls)
    competitors.update(url_companies)
    
    return list(competitors)

def validate_competitor(competitor_name: str, original_company: str) -> Dict:
    """
    Validate a potential competitor by checking:
    1. If it's a real company
    2. If it's in the same industry
    3. If it's not the same as the original company
    """
    # Initialize validation result
    result = {
        "is_valid": False,
        "confidence_score": 0.0,
        "source": "web",
        "industry_match": False
    }
    
    # 1. Basic validation
    if competitor_name.lower() == original_company.lower():
        return result
    
    # 2. Check if it's a real company
    query = f'"{competitor_name}" company'
    confidence = 0.0
    
    urls = safe_google_search(query, max_results=2, delay=1.5)
    
    if urls:
        # Check number of results
        confidence += min(len(urls) * 0.3, 0.6)
        
        # Check if company appears in URLs
        if any(competitor_name.lower() in url.lower() for url in urls):
            confidence += 0.2
        
        # Check for industry match (only if we have good initial confidence)
        if confidence > 0.3:
            original_query = f'"{original_company}" industry sector'
            competitor_query = f'"{competitor_name}" industry sector'
            
            original_urls = safe_google_search(original_query, max_results=1, delay=2.0)
            competitor_urls = safe_google_search(competitor_query, max_results=1, delay=2.0)
            
            if original_urls and competitor_urls:
                # Simple industry match based on URL patterns
                original_domains = [url.split('/')[2] for url in original_urls if len(url.split('/')) > 2]
                competitor_domains = [url.split('/')[2] for url in competitor_urls if len(url.split('/')) > 2]
                
                # If they share similar domain patterns, they might be in the same industry
                if any(domain in competitor_domains for domain in original_domains):
                    confidence += 0.2
                    result["industry_match"] = True
    
    result["confidence_score"] = confidence
    result["is_valid"] = confidence > 0.4
    
    return result 