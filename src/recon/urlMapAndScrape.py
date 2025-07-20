from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import urljoin, urlparse

visited = set()
collected_data = []

def extract_page_info(url):
    base_url = url
    visited.add(base_url)

    print(f"🚀 Crawling: {url}")
    try:
        r = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching {url}: {e}")
        return

    soup = BeautifulSoup(r.text, "html.parser")

    # Meta tags
    title = soup.title.string.strip() if soup.title else ""
    description = ""
    keywords = ""
    for meta in soup.find_all("meta"):
        name = meta.get("name", "").lower()
        if name == "description":
            description = meta.get("content", "")
        elif name == "keywords":
            keywords = meta.get("content", "")

    # Headings h1 to h6 with tag info and text
    headings = []
    for level in range(1, 7):
        tag_name = f"h{level}"
        for tag in soup.find_all(tag_name):
            headings.append({"tag": tag_name, "text": tag.get_text(strip=True)})

    # Paragraphs (limit first 10)
    paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')[:10]]

    # Collect emails
    emails = list(set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', r.text)))

    # Store scraped data
    page_data = {
        "url": url,
        "title": title,
        "description": description,
        "keywords": keywords,
        "headings": headings,
        "paragraphs": paragraphs,
        "emails": emails
    }

    collected_data.append(page_data)

    # Crawl internal links
    for a in soup.find_all("a", href=True):
        href = a["href"]
        full_url = urljoin(url, href)
        parsed = urlparse(full_url)

        # Only follow internal links within the same domain
        if parsed.netloc == urlparse(base_url).netloc:
            # Clean anchor fragments
            full_url = full_url.split('#')[0]
            if full_url not in visited:
                visited.add(full_url)
                extract_page_info(full_url)

    return collected_data





