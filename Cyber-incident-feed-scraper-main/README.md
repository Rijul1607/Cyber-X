# **Cyber-Incident-Feed-Scraper**
### Overview
Cyber-Incident-Feed-Scraper is a tool designed to scrape and collect real-time feeds of cyber incidents specifically related to the Indian cyberspace. Developed as part of a hackathon project, this tool leverages web scraping techniques using Selenium to gather, parse, and store cyber incident data in a structured format.

### Purpose
This project was developed for a hackathon to provide a streamlined method of obtaining up-to-date information on cyber incidents. By focusing on incidents pertinent to Indian cyberspace, this tool helps in identifying potential vulnerabilities and provides quick access to relevant cybersecurity news.

#### Key Features
Real-time Web Scraping: Utilizes Selenium to scrape news and incident data from multiple sources.
Structured Data Output: Organizes scraped data into a structured format for easy consumption.

#### Sample Output
```json
[
    {
        "title": "Vulnerability in D-Link (19 Aug 2024)",
        "description": "A command injection vulnerability has been discovered in D-Link. The affected version is D-Link DI-8100 16.07.\nCVE ID: CVE-2024-7833 (Critical)",
        "link": "https://nvd.nist.gov/vuln/detail/CVE-2024-7833",
        "cve_ids": [
            "CVE-2024-7833"
        ],
        "date": "19 Aug 2024"
    },
    {
        "title": "Red Hat Security Updates (19 Aug 2024)",
        "description": "Red Hat has released security updates to address multiple vulnerabilities in several products.",
        "link": "https://access.redhat.com/errata-search/#/",
        "cve_ids": null,
        "date": "19 Aug 2024"
    },
    {
        "title": "Google Released Security Updates for Chrome (16 Aug 2024)",
        "description": "Google has released Beta channel 128.0.6613.32 Platform version 15964.24.0 for most ChromeOS devices, LTC-126 version 126.0.6478.244 Platform Version 15886.75.0 for most ChromeOS devices and Dev channel 129.0.6658.0 for Windows, Mac and Linux.",
        "link": "https://chromereleases.googleblog.com/",
        "cve_ids": null,
        "date": "16 Aug 2024"
    }
]

```

#### Clone the repository:
`git clone https://github.com/Sahilidc/cyber-incident-feed-scraper.git`
cd cyber-incident-feed-scraper

#### Configuration
Selenium WebDriver: Update the WebDriver path in the script to match your local setup.

#### Contributing
Contributions are welcome! Please open an issue or submit a pull request for any changes or improvements.


