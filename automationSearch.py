import requests
from bs4 import BeautifulSoup
import re
import json
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('SERPAPIKEY')
query = "fire risk assessors uk"

params = {
    "engine": "google",  # We're using Google's engine
    "q": query,  # The query you're searching for
    "api_key": api_key,  # Your API key
    "num": 100,  # Number of results per page (max 100)
    "location": "United Kingdom"  # Optional: restrict results by location
}

response = requests.get("https://serpapi.com/search.json", params=params)

results = response.json()

#Extract URLs from the search results
urls = [] 
for result in results.get("organic_results", []):
    link = result.get("link")
    if link:
        urls.append(link)
        print(f"🔗 {link}")

#ptionally, save the URLs to a file or a variable
with open('gooleScrape.json', 'w') as json_file:
    json.dump(urls, json_file, indent=4)
