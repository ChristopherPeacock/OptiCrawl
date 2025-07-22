import requests
import json
import os
import hashlib
import platform
import sys
from dotenv import load_dotenv
import pathlib

def main(keyword, location, engine):
    # Load .env from SCRAPER/Data/.env
    env_path = pathlib.Path(__file__).resolve().parents[1] / 'Data' / '.env'
    load_dotenv(dotenv_path=env_path)

    api_key = os.getenv("SERPAPIKEY")
    if not api_key:
        print("❌ API key not found in .env file")
        return

    # Pagination state
    pagination_file = pathlib.Path("pagination_state.json")
    if pagination_file.exists():
        with open(pagination_file, 'r') as f:
            state = json.load(f)
            current_page = state.get("start", 0)
    else:
        current_page = 0

    # Load existing scraped URLs
    existing_hashes = set()
    output_file = pathlib.Path("googleScrape.json")
    if output_file.exists():
        with open(output_file, 'r') as f:
            existing_data = json.load(f)
            for batch_data in existing_data.values():
                for url in batch_data:
                    url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
                    existing_hashes.add(url_hash)
    else:
        existing_data = {}

    def get_search_results(start):
        params = {
            "engine": engine,
            "q": keyword,
            "api_key": api_key,
            "num": 100,
            "location": location,
            "start": start
        }
        response = requests.get("https://serpapi.com/search.json", params=params)
        return response.json()

    total_urls_scanned = 0

    while True:
        results = get_search_results(current_page)

        if "organic_results" not in results:
            print("✅ No more results.")
            return 1

        new_urls = []
        for result in results["organic_results"]:
            link = result.get("link")
            if link:
                url_hash = hashlib.md5(link.encode('utf-8')).hexdigest()
                if url_hash not in existing_hashes:
                    new_urls.append(link)
                    existing_hashes.add(url_hash)
                    print(f"🔗 {link}")
                    total_urls_scanned += 1

        if not new_urls:
            print('no new results')
            return -1

        batch_number = len(existing_data) + 1
        existing_data[f"batch_{batch_number}_urls_scanned_{total_urls_scanned}"] = new_urls

        # Save updated data
        with open(output_file, 'w') as f:
            json.dump(existing_data, f, indent=4)

        # Increment pagination
        current_page += 100
        with open(pagination_file, 'w') as f:
            json.dump({'start': current_page}, f)

        print(f"📦 Total URLs Scanned: {total_urls_scanned}")
        if current_page == 300:
            return 1
       
if __name__ == "main":

    main()
