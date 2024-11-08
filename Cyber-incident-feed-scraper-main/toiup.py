import requests
from bs4 import BeautifulSoup
import json
import os
import ssl
import socket

# Define PhishTank API endpoint and API key
# PHISHTANK_API_URL = 'https://checkurl.phishtank.com/checkurl/'
# PHISHTANK_API_KEY = 'your_phishtank_api_key'  # Replace with your PhishTank API key

def is_https(url):
    """Check if the URL uses HTTPS."""
    return url.startswith('https://')

def is_ssl_certificate_valid(url):
    """Check if the SSL certificate of the URL is valid."""
    try:
        parsed_url = requests.utils.urlparse(url)
        hostname = parsed_url.hostname
        port = parsed_url.port or 443
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                ssock.getpeercert()
        return True
    except Exception as e:
        print(f"SSL certificate validation failed: {e}")
        return False

# Define the URL of the webpage to scrape
url = "https://timesofindia.indiatimes.com/topic/cyber-security/news"

# Check HTTPS and SSL certificate
if not is_https(url):
    print("URL does not use HTTPS.")
else:
    if not is_ssl_certificate_valid(url):
        print("SSL certificate is not valid.")
    else:
        # Send a GET request to the webpage
        try:
            response = requests.get(url, verify=True)
            response.raise_for_status()
            
            # Parse the webpage content with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Initialize a list to hold the extracted data
            news_data = []

            # Find all the article containers starting with the class 'uwU81'
            articles = soup.find_all("div", class_="uwU81")

            # Loop through each article and extract the relevant details
            for article in articles:
                # Find the title within the correct nested classes
                title = article.find("div", class_="fHv_i").text.strip() if article.find("div", class_="fHv_i") else None

                # Find the summary within the 'oxXSK o58kM' class
                summary = article.find("p", class_="oxXSK o58kM").text.strip() if article.find("p", class_="oxXSK o58kM") else None

                # Find the link
                link = article.find("a")['href'] if article.find("a") else None
                if link and not link.startswith('http'):
                    link = "https://timesofindia.indiatimes.com" + link  # Complete relative URLs

                # Commented out PhishTank check
                # if link:
                #     is_phishing, status = check_phishing(link)
                #     if is_phishing:
                #         print(f"URL {link} is flagged as phishing: {status}")
                #         continue

                # Find the source and date within the 'ZxBIG' class
                source_date = article.find("div", class_="ZxBIG").text.strip() if article.find("div", class_="ZxBIG") else None
                
                # Initialize author and date variables
                author = None
                date = None

                # Try to extract the author's name and date
                if source_date:
                    parts = source_date.split('/')
                    author = parts[0].strip() if len(parts) > 1 else None
                    date = parts[1].strip() if len(parts) > 1 else source_date

                # Create a dictionary for each news article
                news_item = {
                    "title": title,
                    "summary": summary,
                    "link": link,
                    "author": author,
                    "date": date
                }

                # Append the dictionary to the list
                news_data.append(news_item)

            # Get the Desktop path dynamically
            desktop_path = os.path.expanduser("~/Desktop/cybersecurity_news.json")
            print(f"Saving to: {desktop_path}")

            # Save the extracted data as a JSON file on your Desktop with formatted output
            with open(desktop_path, "w") as json_file:
                json.dump(news_data, json_file, indent=4, separators=(',', ': '))

            print("Scraping completed and data saved to cybersecurity_news.json")

        except requests.RequestException as e:
            print(f"Failed to retrieve the page. Error: {e}")
