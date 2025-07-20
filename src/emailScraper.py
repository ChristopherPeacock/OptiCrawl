import requests
from bs4 import BeautifulSoup
import re
import json
import os
from dotenv import load_dotenv
import time

load_dotenv()

jsonOfEmails = {}

def extract_emails_from_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"⚠️ Failed to fetch {url}: {e}")
        return set()

    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()
    emails = set(re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text))
    return emails
    
def loadListAndExtract():
    # Load list of URLs
    urls = []
    if os.path.exists('googleScrape.json'):
        with open('googleScrape.json', 'r') as json_file:
            urls = json.load(json_file)
            print(f"📄 Loaded {len(urls)} URLs from googleScrape.json.")
    else:
        print("🚫 No file exists.")
        exit()

    for batch, arrays in urls.items():
        print(f"📁 {batch}")
        for url in arrays:
            emails = extract_emails_from_url(url)
            if emails:
                jsonOfEmails[url] = list(emails)
                for email in emails:
                    print(f"📨 {email} <- from {url}")
           
    # Save final results
    with open('emails.json', 'w') as json_file:
        json.dump(jsonOfEmails, json_file, indent=4)
        print(f"\n✅ Saved {len(jsonOfEmails)} results to emails.json.")    
    
if __name__ == "__main__":
    loadListAndExtract()
