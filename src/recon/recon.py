import requests
from bs4 import BeautifulSoup
import os
import re
from urllib.parse import urlparse
from urlMapAndScrape import extract_page_info
from pathlib import Path
from scrapeLinkedin import linkedinInfoScraper
from datetime import datetime
import json

def extractCompanyName(soup):
    pass

def scrapedWebPageInfo(soup):
    pass

def extractLinkedUrls(soup):
    urls = []
    for a_tag in soup.find_all('a', href=True):
        urls.append(a_tag['href'])
    return urls

def filter(arrayOfBackLinks, url):
    companyDomain = url.lower()

    linkedInUrls = []
    emails = []
    backLinks = []

    emailPattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    linkedInPattern = r'https?://(?:www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+/?'
    notUsefulEmailPattern = r'^(info|support|admin|sales)@'

    for backlink in arrayOfBackLinks:
        backlink_lower = backlink.lower()

        # LinkedIn retrieval
        linkedMatches = re.findall(linkedInPattern, backlink_lower)
        linkedInUrls.extend(linkedMatches)

        # Email patterns
        emailMatches = re.findall(emailPattern, backlink_lower)
        for email in emailMatches:
            if not re.match(notUsefulEmailPattern, email):
                emails.append(email)

        parsed = urlparse(backlink_lower)
        if companyDomain not in parsed.netloc:
            backLinks.append(backlink)

    return {
        "Possible_Competitors": list(set(backLinks)),
        "emails": list(set(emails)),             
        "linkedin_profiles": list(set(linkedInUrls))
    }

def reteriveInformation (content, url):
    soup = BeautifulSoup(content, 'html.parser')
    companyName = extractCompanyName(soup)
    arrayOfbackLinks = extractLinkedUrls(soup)
    contactLists = filter(arrayOfbackLinks, url)
    linkedinRecon = linkedinInfoScraper(url)
    webPageInfomation = scrapedWebPageInfo(soup)
    fullWebSiteMapedAndScraped = extract_page_info(url)
    fullWebSiteContent = fullWebSiteMapedAndScraped
    
    print('Recon done, building up report ')

    token_heavy_markdown_report = f"""
        ## This is a company report that was gathered with an OSINT tool.

        # The following data was up to date when it was gathered on {datetime.now().strftime('%Y-%m-%d')}.

        # Company name is: { companyName or 'no company name able to be gathered but the url is:', {url}}.
         
        # Company Url is: {url}, 
        # That information is there to confirm the company name via url domain and can be used as a second look up if needed.

        # The OSINT tool check for any back links that could show tha our target customer are using 3rd part services either in the same sector as us or not: {contactLists['Possible_Competitors'] or 'No competitor links was found'}.
        
        #These are the Emails the tool extrcted and they have been filtered for more accurracy: {contactLists["emails"] or 'No Champion emails could be found'}.

        #These are the linkedin urls that was found on the companys website {contactLists["linkedin_profiles"] or 'no linkedin profile links was found'},
        #Here is the information found on the companys linkedin profle {linkedinRecon or 'no information was able to be scraped'}.

        #This is all the information gathered that we found on the company - {webPageInfomation or 'no information was able to be scraped'}.

        #This is everything we found on the entire website of the compay that can be used to get full context of he company {fullWebSiteContent or 'no information could be scraped'}.


        ##This report was produced by a OSINT tool called opti-crawl and all data gathered was open t public and no malicouse coding was used to gether this information.
    """

    light_token_markdown_report = f"""
        ## This is a company report that was gathered with an OSINT tool.

        # The following data was up to date when it was gathered on {datetime.now().strftime('%Y-%m-%d')}.

        # Company name is: { companyName or 'no company name able to be gathered but the url is:', {url}}.
         
        # Company Url is: {url}, 
        # That information is there to confirm the company name via url domain and can be used as a second look up if needed.

        # The OSINT tool check for any back links that could show tha our target customer are using 3rd part services either in the same sector as us or not: {contactLists['Possible_Competitors'] or 'No competitor links was found'}.
        
        #These are the Emails the tool extrcted and they have been filtered for more accurracy: {contactLists["emails"] or 'No Champion emails could be found'}.

        #These are the linkedin urls that was found on the companys website {contactLists["linkedin_profiles"] or 'no linkedin profile links was found'},
        #Here is the information found on the companys linkedin profle {linkedinRecon or 'no information was able to be scraped'}.

        #This is all the information gathered that we found on the company: {webPageInfomation or 'no information was able to be scraped'}.

        ##This report was produced by a OSINT tool called opti-crawl and all data gathered was open t public and no malicouse coding was used to gether this information.
    """


    # json report 
    token_heavy_json_report = {
        "report description": {
            "title": "This is a company report that was scraped with an OSINT tool",
            "description": f"The following data was up to date when it was scraped on {datetime.now().strftime('%Y-%m-%d')}"
        },
        "company_name": {
            "description": "This is the companys name that was extarcted from the companys url ",
            "company-name": companyName or 'no company name was passed'
        },
        "url": {
            "description": "This information has been passed in directly and not scraped",
            "url_notes": "This is the company url if needed for a second look up",
            "company_url": url
        },
        "competitors": {
            "description": "This information has been scraped and filtered for accurancy",
            "competitor_notes": "This is possibly our competitors as there other company URls and information",
            "possible_competitor_emails": contactLists['Possible_Competitors'] or 'No competitor links was found' 
        },
        "target_market_emails": {
            "description": "these emails have been scraped and filtered for accurancy",
            "target_emails_note": "These are the emails we will need to target for our email",
            "decision_makers_emails_found": contactLists["emails"] or 'No Champion emails could be found'
        },
        "target_linkedin_links": {
            "description": "This information has been scraped and filtered for accurancy",
            "linkedin_notes": "These links where taken as a possible way of gathering more information on our customers",
            "linkedin_links_found": contactLists["linkedin_profiles"] or 'no linkedin profile links was found'
        },
        "target_linkedin_scraped_info": {
            "description": "This information has been scraped and filtered for accurancy",
            "target_linkedin_info": "This infomation was scraped directly from {target_linkedin_links}",
            "linkedin_info": linkedinRecon or 'no information was able to be scraped'
        },
        "company_infomation" : {
            "description": "This information has been scraped and filtered for accurancy",
            "company_infomation_notes": "This info is a short description of who are target is and who there about",
            "company_infomation" : webPageInfomation or 'no information was able to be scraped'
        },
        "full_customer_map" : {
            "description": "This information has been scraped and filtered for accurancy",
            "full_customer_map_notes": "This is a json map of the target customer for full context across all sub domains",
            "full_maped_and_scraped_Company_Website": fullWebSiteContent or 'no information could be scraped'
        },  
    }

    light_token_json_report = {
        "report description": {
            "title": "This is a company report that was scraped with an OSINT tool",
            "description": f"The following data was up to date when it was scraped on {datetime.now().strftime('%Y-%m-%d')}"
        },
        "url": {
            "description": "This information has been passed in directly and not scraped",
            "url_notes": "This is the company url if needed for a second look up",
            "company_url": url
        },
        "competitors": {
            "description": "This information has been scraped and filtered for accurancy",
            "competitor_notes": "This is possibly our competitors as there other company URls and information",
           "possible_competitor_emails": contactLists['Possible_Competitors'] or 'No competitor links was found'  
        },
        "target_market_emails": {
            "description": "these emails have been scraped and filtered for accurancy",
            "target_emails_note": "These are the emails we will need to target for our email",
            "decision_makers_emails_found": contactLists["emails"] or 'No Champion emails could be found'
        },
        "target_linkedin_links": {
            "description": "This information has been scraped and filtered for accurancy",
            "linkedin_notes": "These links where taken as a possible way of gathering more information on our customers",
             "linkedin_links_found": contactLists["linkedin_profiles"] or 'no linkedin profile links was found'
        },
        "target_linkedin_scraped_info": {
            "description": "This information has been scraped and filtered for accurancy",
            "target_linkedin_info": "This infomation was scraped directly from {target_linkedin_links}",
            "linkedin_info": linkedinRecon or 'no information was able to be scraped'
        },
        "company_infomation" : {
            "description": "This information has been scraped and filtered for accurancy",
            "company_infomation_notes": "This info is a short description of who are target is and who there about",
            "company_infomation" : webPageInfomation or 'no information was able to be scraped' 
        },
    }

    def sanitize_url(url):
        url = re.sub(r'https?://', '', url)
        return re.sub(r'[^a-zA-Z0-9._-]', '_', url)
    
    desktopPath = Path.home()
    base_folder = desktopPath / "Desktop/MarketingReport"
    sanitized_folder = sanitize_url(url)
    full_report_path = base_folder / sanitized_folder
    if not full_report_path.exists():
        try:
            print(f"Creating folder at {full_report_path}")
            full_report_path.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            print(f"Could not create folder.\nReason: {e.strerror}")

    # Define file paths
    token_heavy_json = full_report_path / "heavy_report.json"
    light_token_json = full_report_path / "light_report.json"
    token_heavy_markdown = full_report_path / "heavy_report.md"
    light_token_markdown = full_report_path / "light_report.md"

    # Write Markdown files
    with open(token_heavy_markdown, 'w', encoding='utf-8') as f:
        f.write( token_heavy_markdown_report)

    with open(light_token_markdown, 'w', encoding='utf-8') as f:
        f.write(light_token_markdown_report)

    # Write JSON files
    with open(token_heavy_json, 'w', encoding='utf-8') as f:
        json.dump(token_heavy_json_report, f, indent=4)

    with open(light_token_json, 'w', encoding='utf-8') as f:
        json.dump(light_token_json_report, f, indent=4)
    
def erroredUrls ():
    pass 

def extractContent(url):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Referer": "https://www.google.com/",
    "Connection": "keep-alive",
    }
    try: 
        response = requests.get(url, headers=headers, timeout=10)

        def serverResponse (code):
            if 200 <= code < 300:
                reteriveInformation(response.text, url)
                return 'sucess'
            elif 400 <= code < 500:
                erroredUrls(response.url)
                return 'client error'
            else:
                return f"unkown error: {code}"

        serverResponse(response.status_code) 
        
    except requests.exceptions as e:
        print(f"failed to connect to {url}: {e}")
        return 
    
    


