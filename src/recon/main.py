import requests
from bs4 import BeautifulSoup
import os
import re
from urllib.parse import urlparse
from recon.urlMapAndScrape import extract_page_info
from pathlib import Path
from recon.scrapeLinkedin import linkedinInfoScraper
from core.shared import dnsChecker
import json
import time

# map all urls and back links 
# I can could scrape look for anker tags and then follow them? 
# match emails found on web page and compare if diffrent bring forward for evaulation
# can i do a DNS chaeck on a domain name 
# check who there. could do sit codes?

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
    #companyName = extractCompanyName(soup)
    arrayOfbackLinks = extractLinkedUrls(soup)
    contactLists = filter(arrayOfbackLinks, url)
    linkedinRecon = linkedinInfoScraper(url)
    #webPageInfomation = ScrapedWebPageInfo(soup)
    fullWebSiteMapedAndScraped = extract_page_info(url)


    #veriables to add into the report
    possiblecDomainsFound = contactLists['Possible_Competitors'] or 'No competitor links was found'
    decisionMakersEmailsFound = contactLists["emails"] or 'No Champion emails could be found'
    linkedInProfilesFound = contactLists["linkedin_profiles"] or 'no linkedin profile links was found'
    linkedinInformation = linkedinRecon or 'no information was able to be scraped'
    fullWebSiteContent = fullWebSiteMapedAndScraped
    print('Recon done, building up report ')
    # use all veribales to make a markdown report

    heavyMarkDownReport = f"""
    ## This is a report on {url or 'No url was given'} 
    
    # During the the recon phase we found tryed to find some competitor back links.
    # This is who possibly our customers are working with: {possiblecDomainsFound}.

    # We also scraped and filtered champion emails. 
    # Champions are people who have power to move finaical decions for the company
    # {decisionMakersEmailsFound}

    # Along side this we tryed to find the linkedin profiles of who are on the company page
    # People on company page are normaly important so we tryed to collect there linkedin profiles for futher recon
    # {linkedInProfilesFound}

    # We also tryed to scrape the data found on linkedin {linkedinInformation}

    # Here is the the full context of the company that was scraped.
    # {fullWebSiteContent}


    """

    lightMarkDownReport = f"""
    ## This is a report on {url or 'No url was given'} 
    
    # During the the recon phase we found tryed to find some competitor back links.
    # This is who possibly our customers are working with: {possiblecDomainsFound}.

    # We also scraped and filtered champion emails. 
    # Champions are people who have power to move finaical decions for the company
    # {decisionMakersEmailsFound}

    # Along side this we tryed to find the linkedin profiles of who are on the company page
    # People on company page are normaly important so we tryed to collect there linkedin profiles for futher recon
    # {linkedInProfilesFound}

    # We also tryed to scrape the data found on linkedin {linkedinInformation}

   


    """

    # json report 
    token_heavy_json_report = {
        "url": {
            "description": "This information has been passed in directly and not scraped",
            "url_notes": "This is the company url if needed for a second look up",
            "company_url": url
        },
        "competitors": {
            "description": "This information has been scraped and filtered for accurancy",
            "competitor_notes": "This is possibly our competitors as there other company URls and information",
            "possible_competitor_emails": possiblecDomainsFound 
        },
        "target_market_emails": {
            "description": "these emails have been scraped and filtered for accurancy",
            "target_emails_note": "These are the emails we will need to target for our email",
            "decision_makers_emails_found": decisionMakersEmailsFound
        },
        "target_linkedin_links": {
            "description": "This information has been scraped and filtered for accurancy",
            "linkedin_notes": "These links where taken as a possible way of gathering more information on our customers",
            "linkedin_links_found": linkedInProfilesFound,
        },
        "target_linkedin_scraped_info": {
            "description": "This information has been scraped and filtered for accurancy",
            "target_linkedin_info": "This infomation was scraped directly from {target_linkedin_links}",
            "linkedin_info": linkedinInformation
        },
        "company_infomation" : {
            "description": "This information has been scraped and filtered for accurancy",
            "company_infomation_notes": "This info is a short description of who are target is and who there about",
            # "company_infomation" : webPageInfomation, 
        },
        "full_customer_map" : {
            "description": "This information has been scraped and filtered for accurancy",
            "full_customer_map_notes": "This is a json map of the target customer for full context across all sub domains",
            "full_maped_and_scraped_Company_Website": fullWebSiteContent
        },  
    }

    light_token_json_report = {
        "url": {
            "description": "This information has been passed in directly and not scraped",
            "url_notes": "This is the company url if needed for a second look up",
            "company_url": url
        },
        "competitors": {
            "description": "This information has been scraped and filtered for accurancy",
            "competitor_notes": "This is possibly our competitors as there other company URls and information",
            "possible_competitor_emails": possiblecDomainsFound 
        },
        "target_market_emails": {
            "description": "these emails have been scraped and filtered for accurancy",
            "target_emails_note": "These are the emails we will need to target for our email",
            "decision_makers_emails_found": decisionMakersEmailsFound
        },
        "target_linkedin_links": {
            "description": "This information has been scraped and filtered for accurancy",
            "linkedin_notes": "These links where taken as a possible way of gathering more information on our customers",
            "linkedin_links_found": linkedInProfilesFound,
        },
        "target_linkedin_scraped_info": {
            "description": "This information has been scraped and filtered for accurancy",
            "target_linkedin_info": "This infomation was scraped directly from {target_linkedin_links}",
            "linkedin_info": linkedinInformation
        },
        "company_infomation" : {
            "description": "This information has been scraped and filtered for accurancy",
            "company_infomation_notes": "This info is a short description of who are target is and who there about",
            # "company_infomation" : webPageInfomation, 
        },
    }

    
    # Define the desktop folder
    desktopPath = Path.home()
    filePath = desktopPath / "Desktop/MarketingReport"

# Create the folder if it doesn't exist
    if not os.path.exists(filePath):
        try:
            print(f"Creating folder in {filePath}")
            os.makedirs(filePath, exist_ok=True)
        except OSError as e:
            print(f"Couldn't create folder on the Desktop.\nReason: {e.strerror}\nPlease check your permissions or available space.")

    # Define file paths
    token_heavy_json_report_file = os.path.join(filePath, "heavyJsonReport.json")
    light_token_json_report_file = os.path.join(filePath, "lightJsonReport.json")
    heavy_mark_down_report_file = os.path.join(filePath, 'heavMarkdownReport.md')
    light_mark_down_report_file = os.path.join(filePath, 'lightMarkDownRepor.md')

    # Save the JSON files
    with open(token_heavy_json_report_file, 'w') as file:
        json.dump(token_heavy_json_report, file, indent=4)

    with open(light_token_json_report_file, 'w') as file:
        json.dump(light_token_json_report, file, indent=4)
    
    with open(heavy_mark_down_report_file, "w") as file:
        file.write(heavyMarkDownReport)
    
    with open(light_mark_down_report_file, 'w') as file:
        file.write(heavy_mark_down_report_file)
    
    print(f"Reports saved @: {filePath}")
    time.sleep(5)

    
def erroredUrls ():
    pass 

def recon():

    url = input("Enter Url of target")
    confirmedUrl = dnsChecker(url)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive",
    }
    try: 
        response = requests.get(confirmedUrl, headers=headers, timeout=10)

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
    

if __name__ == '__main__':
    recon('www.opticompliance.co.uk')