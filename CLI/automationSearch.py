import requests
import json
import os
import hashlib
import platform
import sys
from dotenv import load_dotenv
import pathlib


def main(keyWord, location, engine):
    
    load_dotenv()
    
    urlsScanned = 0
    
    current_page = 0 
    
    # Go up from CLI to root (SCRAPER), then into Data/.env
    env_path = pathlib.Path(__file__).resolve().parents[1] / 'Data' / '.env'
    load_dotenv(dotenv_path=env_path)

    api_key = os.getenv("SERPAPIKEY")

    query = keyWord 

    def get_search_results(start):
        params = {
            "engine": engine,  
            "q": query, 
            "api_key": api_key,  
            "num": 100,  
            "location": location, 
            "start": start 
        }
        response = requests.get("https://serpapi.com/search.json", params=params)
        return response.json()

    # Use the correct path joining approach
    existing_hashes = set()
    urlScrapedPath = pathlib.Path('Data/')
    file_path = urlScrapedPath / 'googleScrape.json'  # Proper path joining with pathlib

    if os.path.exists(file_path):
        with open(file_path, 'r') as json_file:
            existing_data = json.load(json_file)
            # Add all previously scraped URLs to the existing_hashes set
            for batch_key, batch_data in existing_data.items():
                for url in batch_data:
                    url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
                    existing_hashes.add(url_hash)
    else:
        existing_data = {}

    pagination_path = urlScrapedPath/'pagination_state.json'
    if os.path.exists(pagination_path):
        with open(pagination_path, 'r') as f:
            current_page = json.load(f).get('start', 0)
    else:
        current_page = 0

    
    def is_duplicate(url):
        url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
        return url_hash in existing_hashes

    total_urls_scanned = 0

    while True:
    
        results = get_search_results(current_page)

        print(json.dumps(results, indent=2)) 
        
        if "organic_results" not in results:
            print("No more results found.")
            return 1
        
        new_urls = []

        for result in results.get("organic_results", []):
            link = result.get("link")
            if link and not is_duplicate(link):
                total_urls_scanned += 1
                new_urls.append(link)
                
                existing_hashes.add(hashlib.md5(link.encode('utf-8')).hexdigest())
                print(f"🔗 {link}")

        if not new_urls:
            print("No new URLs found in this batch.")
            return -1
        
        current_page += 100
        
        batch_number = len(existing_data) + 1  
        data_with_batch = {f"batch_{batch_number} , _urls_scanned_{total_urls_scanned}": new_urls}

        existing_data.update(data_with_batch)

        with open('googleScrape.json', 'w') as json_file:
            json.dump(existing_data, json_file, indent=4)

        with open('pagination_state.json', 'w') as f:
            json.dump({'start': current_page}, f)

        print(f"Total URLs Scanned: {total_urls_scanned}")

        return 1

if __name__ == "__main__":
    main()