import requests
import ssl
import socket
import json
import os
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import io
from collections import Counter

# Helper function to check if a URL uses HTTPS
def is_https(url):
    """Check if the URL uses HTTPS."""
    return url.startswith('https://')

# Helper function to clean text
def clean_text(text):
    text = text.replace('\u2219', '').encode('utf-8', 'ignore').decode('utf-8')
    return text

# Helper function to check SSL certificate validity
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

# Categorizing incidents by sector
def categorize_by_sector(news_data):
    sectors = ['Healthcare', 'Finance', 'Government', 'Retail']
    sector_count = {sector: 0 for sector in sectors}
    
    for article in news_data:
        title = article['title'].lower() if article['title'] else ''
        for sector in sectors:
            if sector.lower() in title:
                sector_count[sector] += 1
                break
    return sector_count

# Categorizing incidents by APTs
def categorize_by_apt(news_data):
    apts = ['APT29', 'APT41', 'Lazarus Group']
    apt_count = {apt: 0 for apt in apts}
    
    for article in news_data:
        title = article['title'].lower() if article['title'] else ''
        for apt in apts:
            if apt.lower() in title:
                apt_count[apt] += 1
                break
    return apt_count

# Categorizing incidents by strategic issues
def categorize_by_strategic_issue(news_data):
    issues = ['Data Breaches', 'Ransomware', 'Phishing']
    issue_count = {issue: 0 for issue in issues}
    
    for article in news_data:
        summary = article['summary'].lower() if article['summary'] else ''
        for issue in issues:
            if issue.lower() in summary:
                issue_count[issue] += 1
                break
    return issue_count

# Generate insights from the scraped data
def generate_cyber_insights(news_data):
    insights = {}
    insights['incidents_by_sector'] = categorize_by_sector(news_data)
    insights['apts_involved'] = categorize_by_apt(news_data)
    insights['strategic_issues'] = categorize_by_strategic_issue(news_data)
    return insights

# Web scraping and insight generation
url = "https://cyware.com/search?search=india"

# Check if HTTPS and SSL certificate are valid
if not is_https(url):
    print("URL does not use HTTPS.")
elif not is_ssl_certificate_valid(url):
    print("SSL certificate is not valid.")
else:
    try:
        # Setup Selenium WebDriver
        options = Options()
        options.add_argument("--headless")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # Fetch the URL
        driver.get(url)
        time.sleep(10)

        # Extract article elements
        articles = driver.find_elements(By.CSS_SELECTOR, "div.cy-panel__body")

        print(f"Found {len(articles)} articles.")

        # Process each article and scrape data
        news_data = []
        for article in articles:
            try:
                title_element = article.find_element(By.CSS_SELECTOR, ".cy-card__title")
                title = clean_text(title_element.text.strip()) if title_element else None

                summary_element = article.find_element(By.CSS_SELECTOR, ".cy-card__description")
                summary = clean_text(summary_element.text.strip()) if summary_element else None

                link_element = article.find_element(By.CSS_SELECTOR, "a")
                link = link_element.get_attribute("href") if link_element else None

                # Find the publication date (if available)
                date_elements = article.find_elements(By.CSS_SELECTOR, ".cy-card__meta")
                date = None
                for elem in date_elements:
                    date_text = clean_text(elem.text.strip())
                    if re.match(r'\w+ \d{1,2}, \d{4}', date_text):
                        date = date_text
                        break

                # Append the scraped data to the list
                news_item = {
                    "title": title,
                    "summary": summary,
                    "link": link,
                    "date": date
                }
                news_data.append(news_item)

            except Exception as e:
                print(f"Error processing an article: {e}")

                # Clean the scraped data
        for article in news_data:
            article['title'] = clean_text(article.get('title', ''))
            article['summary'] = clean_text(article.get('summary', ''))

        # Save scraped news data to a JSON file
        try:
            desktop_path = os.path.expanduser("Cyber-incident-feed-scraper-main/cyware_news.json")
            if os.path.exists('cyware_news.json'):
                open('cyware_news.json', 'w').close()  # Clear file before writing
            with io.open(desktop_path, "w", encoding="utf-8") as json_file:
                json.dump(news_data, json_file, indent=4, separators=(',', ': '), ensure_ascii=False)
            print("News data saved to cyware_news.json.")
        except UnicodeEncodeError as e:
            print(f"Encoding error: {e.object[e.start:e.end]} at position {e.start}")

        # Connect to MongoDB
        client = MongoClient("mongodb://localhost:27017/")
        db = client["cyber_news_db"]
        collection_news = db["cyware_news"]
        collection_news.delete_many({})  # Clear old data

        # Insert scraped data into MongoDB
        if news_data:
            collection_news.insert_many(news_data)
            print("News data inserted into MongoDB.")
        else:
            print("No news data found to insert into MongoDB.")

        # Generate insights from the scraped data
        insights = generate_cyber_insights(news_data)
        print("Generated Insights:", insights)

        # Save insights to a JSON file
        try:
            insights_path = os.path.expanduser("cyber_news_insights.json")
            with io.open(insights_path, "w", encoding="utf-8") as insights_file:
                json.dump(insights, insights_file, indent=4, separators=(',', ': '), ensure_ascii=False)
            print("Insights saved to cyber_news_insights.json.")
        except Exception as e:
            print(f"Error writing to insights JSON file: {e}")

        # Insert insights into MongoDB
        collection_insights = db["cyber_news_insights"]
        collection_insights.delete_many({})  # Clear old insights
        if insights:
            collection_insights.insert_one(insights)
            print("Insights inserted into MongoDB.")
        else:
            print("No insights to insert into MongoDB.")

    except Exception as e:
        print(f"An error occurred during scraping or database operations: {e}")

    finally:
        # Close the WebDriver
        driver.quit()

    print("Scraping completed, data saved to cyware_news.json and insights saved to cyber_news_insights.json.")
