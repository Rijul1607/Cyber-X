import requests
import ssl
import socket
import json
import os
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

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
url = "https://nciipc.gov.in/alerts_advisories_more_2023.html"

# Check HTTPS and SSL certificate
if not is_https(url):
    print("URL does not use HTTPS.")
elif not is_ssl_certificate_valid(url):
    print("SSL certificate is not valid.")
else:
    # Initialize the Firefox WebDriver
    driver = webdriver.Firefox()

    # Open the webpage
    driver.get(url)

    # Allow the page to load
    time.sleep(2)

    # Find all the list items containing vulnerability data
    vulnerability_elements = driver.find_elements(By.CLASS_NAME, "liList")

    # Initialize a list to hold the extracted data
    vulnerabilities = []

    # Regular expressions to match the CVE ID and date
    cve_pattern = re.compile(r"CVE-\d{4}-\d{4,7}")
    date_pattern = re.compile(r"\(\d{2} \w+ \d{4}\)")

    # Loop through each element and extract the relevant details
    for elem in vulnerability_elements:
        title = elem.find_element(By.TAG_NAME, "b").text
        description = elem.find_element(By.CLASS_NAME, "advisoryFont").text.strip()
        link = elem.find_element(By.TAG_NAME, "a").get_attribute("href")
        
        # Extract the CVE IDs and date from the text
        cve_ids = cve_pattern.findall(description)
        date_match = date_pattern.search(title)
        date = date_match.group(0) if date_match else None
        
        # Create a dictionary for each vulnerability
        vulnerability = {
            "title": title,
            "description": description,
            "link": link,
            "cve_ids": cve_ids if cve_ids else None,
            "date": date.strip("()") if date else None
        }
        
        # Append the dictionary to the list
        vulnerabilities.append(vulnerability)

    # Get the Desktop path dynamically
    desktop_path = os.path.expanduser("~/Desktop/vulnerabilities23.json")

    # Save the extracted data as a JSON file on your Desktop with formatted output
    with open(desktop_path, "w") as json_file:
        json.dump(vulnerabilities, json_file, indent=4, separators=(',', ': '))

    # Close the WebDriver
    driver.close()

    print("Scraping completed and data saved to vulnerabilities23.json")
