import requests
import json
import os
import hashlib
import platform
import sys
from dotenv import load_dotenv
from banner import show_banner

def main():
    
    load_dotenv()

    urlsScanned = 0
    current_page = 0  # Default starting point

    api_key = os.getenv('SERPAPIKEY')
    query = "fire risk assessors uk,"

    # Function to get the next batch of search results based on pagination
    def get_search_results(start):
        params = {
            "engine": "google",  # We're using Google's engine
            "q": query,  # The query you're searching for
            "api_key": api_key,  # Your API key
            "num": 100,  # Number of results per page (max 100)
            "location": "United Kingdom",  # Optional: restrict results by location
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

    # Start pagination from the saved or default starting point (current_page)
    while True:
        # Get the next set of search results
        results = get_search_results(current_page)

        # Check if there are results to process
        if "organic_results" not in results:
            print("No more results found.")
            break

        # New URLs to be added
        new_urls = []

        # Process the search results
        for result in results.get("organic_results", []):
            link = result.get("link")
            if link and not is_duplicate(link):
                total_urls_scanned += 1
                new_urls.append(link)
                # Add the URL hash to the set of existing hashes
                existing_hashes.add(hashlib.md5(link.encode('utf-8')).hexdigest())
                print(f"🔗 {link}")

        # If no new URLs are found, break the loop (no more new results)
        if not new_urls:
            print("No new URLs found in this batch.")
            break

        # Increment the start value to get the next set of results (pagination)
        current_page += 100

        # Add the new batch of URLs to the existing data
        batch_number = len(existing_data) + 1  # Increment the batch number based on the existing data length
        data_with_batch = {f"batch_{batch_number} , _urls_scanned_{total_urls_scanned}": new_urls}

        # Append the new data to the existing JSON data
        existing_data.update(data_with_batch)

        # Write the updated data back to the JSON file
        with open('googleScrape.json', 'w') as json_file:
            json.dump(existing_data, json_file, indent=4)

        # Save the current pagination state (current_page) to resume later
        with open('pagination_state.json', 'w') as f:
            json.dump({'start': current_page}, f)

    print(f"Total URLs Scanned: {total_urls_scanned}")

main()