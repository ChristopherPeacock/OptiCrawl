import requests
from bs4 import BeautifulSoup
import re
import json

jsonOfEmails = {}

def extract_emails_from_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()
    emails = set(re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text))
    return emails

# Load your list of URLs
with open('results.json', 'r') as file:
    data = json.load(file)

print("Emails found:")

# Iterate and collect results properly
for entry in data:
    url = entry.get('url')
    if url:
        emails = extract_emails_from_url(url)
        if emails:
            jsonOfEmails[url] = list(emails)
            for email in emails:
                print(f"{email} ← from {url}")

# Save all results after loop ends
with open('emails.json', 'w') as json_file:
    json.dump(jsonOfEmails, json_file, indent=4)
    
    