from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

def get_core_domain(url):
    parsed = urlparse(url)
    host = parsed.hostname or url
    parts = host.split('.')
    if len(parts) >= 3 and parts[-2] in ['co', 'com', 'org', 'net']:
        return parts[-3]
    elif len(parts) >= 2:
        return parts[-2]
    else:
        return parts[0]

def extract_linkedin_about_section(soup):
    data = {}
    fields = [
        "website",
        "industry",
        "size",
        "headquarters",
        "organizationType",
        "founderOn",
        "specialties"
    ]

    for field in fields:
        element = soup.find(attrs={"data-test-id": f"about-us__{field}"})
        if element:
            data[field] = element.get_text(strip=True)
        else:
            data[field] = None
    return data

def linkedinInfoScraper(urls):
    if isinstance(urls, str):
        urls = [urls]

    for url in urls:
        slug = get_core_domain(url)
        linkedinUrl = f"https://www.linkedin.com/company/{slug}"
        print(f"🚀 Trying: {linkedinUrl}")

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com/",
            "Connection": "keep-alive",
        }

        try:
            response = requests.get(linkedinUrl, headers=headers, timeout=10)
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to fetch {linkedinUrl}: {e}")
            continue

        if response.status_code != 200:
            print(f"⚠️ LinkedIn returned status code {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        linkedinFields = extract_linkedin_about_section(soup)

        linkedin_page_data = {
            "company_url": url or False,
            "linkedin_url": linkedinUrl or False,
            "description": 'This is the data collected from the company linkedin profile.',
            "linkedin_fields": linkedinFields or False,
            "linkedin_content" : soup or False
        }

        return linkedin_page_data 


