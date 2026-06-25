#!/usr/bin/env python3
"""
Consultant Agent (konsult.py) v0.1
Crawl a company website and diagnose automation potential.
"""

import os
import sys
import argparse
import yaml
import requests
from bs4 import BeautifulSoup

def crawl_site(url):
    """
    Crawls the main page of the website and attempts to find subpages (e.g. About, Contact, Services).
    """
    print(f"[*] Crawling website: {url}")
    try:
        response = requests.get(url, timeout=10, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        response.raise_for_status()
    except Exception as e:
        print(f"[!] Error fetching {url}: {e}", file=sys.stderr)
        return {"html": "", "text": "", "subpages": []}

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract text content
    text_content = soup.get_text(separator=' ', strip=True)
    
    # Simple subpage discovery (limit to 5 internal links)
    subpages = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('/') or url in href:
            full_url = href if href.startswith('http') else f"{url.rstrip('/')}/{href.lstrip('/')}"
            if full_url not in subpages and len(subpages) < 5:
                subpages.append(full_url)
                
    return {
        "html": response.text,
        "text": text_content,
        "subpages": subpages
    }

def analyze_with_llm(site_data):
    """
    Call LLM to classify industry, tech stack, and find automation potential.
    Currently returns a placeholder structure until LLM API keys are configured.
    """
    print("[*] Running diagnosis via LLM (placeholder)...")
    
    # TODO: Implement OpenAI / Anthropic API call here using:
    # api_key = os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    
    # Mock data output representing the expected structure
    report = {
        "company": "Placeholder Company AB",
        "url": "https://example.se",
        "industry": "accounting",
        "estimated_size": "10-20 employees",
        "tech_stack": ["Fortnox", "Slack", "Google Workspace"],
        "automation_potential": [
            {
                "process": "invoice management",
                "signal": "About page mentions manual invoice handling",
                "priority": 1,
                "time_savings_hours_per_week": 8
            },
            {
                "process": "customer support",
                "signal": "FAQ with 40+ questions, no chat module",
                "priority": 2,
                "time_savings_hours_per_week": 5
            }
        ]
    }
    return report

def main():
    parser = argparse.ArgumentParser(description="styde.ai Consultant Agent v0.1")
    parser.add_argument("url", help="Company website URL (e.g. https://example.se)")
    parser.add_argument("-o", "--output", help="Path to save YAML report (default: report.yaml)", default="report.yaml")
    args = parser.parse_args()

    # 1. Crawl
    site_data = crawl_site(args.url)
    
    # 2. Diagnose & Classify
    report = analyze_with_llm(site_data)
    report["url"] = args.url
    
    # 3. Output
    yaml_wrapper = {"test_audit": report}
    
    # Write to terminal
    print("\n=== AUDIT REPORT ===")
    print(yaml.dump(yaml_wrapper, default_flow_style=False, allow_unicode=True))
    
    # Write to file
    with open(args.output, 'w', encoding='utf-8') as f:
        yaml.dump(yaml_wrapper, f, default_flow_style=False, allow_unicode=True)
    print(f"[*] Report successfully saved to {args.output}")

if __name__ == "__main__":
    main()
