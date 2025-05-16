import requests
import json
import os
import hashlib
import platform
import sys
from dotenv import load_dotenv


def main(keyWord, location, engine):
    
    load_dotenv()
    
    urlsScanned = 0
    
    current_page = 0  # Default starting point
    
    api_key = os.getenv('SERPAPIKEY')
    
    query = keyWord  # The search query you want to use

    # Function to get the next batch of search results based on pagination
    def get_search_results(start):
        params = {
            "engine": engine,  # We're using Google's engine
            "q": query,  # The query you're searching for
            "api_key": api_key,  # Your API key
            "num": 100,  # Number of results per page (max 100)
            "location": location,  # Optional: restrict results by location
            "start": start  # Pagination: indicate the starting point
        }
        response = requests.get("https://serpapi.com/search.json", params=params)
        return response.json()

    # Load existing data from the JSON file if it exists
    existing_hashes = set()
    if os.path.exists('googleScrape.json'):
        with open('googleScrape.json', 'r') as json_file:
            existing_data = json.load(json_file)
            # Add all previously scraped URLs to the existing_hashes set
            for batch_key, batch_data in existing_data.items():
                for url in batch_data:
                    url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
                    existing_hashes.add(url_hash)
    else:
        existing_data = {}

    # Load last known pagination state (starting point)
    if os.path.exists('pagination_state.json'):
        with open('pagination_state.json', 'r') as f:
            current_page = json.load(f).get('start', 0)
    else:
        current_page = 0  # Start at page 0 if no state is saved

    # Function to check if a URL has been scanned already
    def is_duplicate(url):
        url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
        return url_hash in existing_hashes

    # Keep track of how many URLs we've scanned
    total_urls_scanned = 0

    while True:
    
        results = get_search_results(current_page)

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