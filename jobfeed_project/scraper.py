import os
import django
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobfeed_project.settings')
django.setup()

from jobfeed.models import Job

def is_recent_job(date_posted_text):
    now = datetime.now()
    if "Just posted" in date_posted_text or "Today" in date_posted_text:
        return True
    elif "day" in date_posted_text:
        days_ago = int(date_posted_text.split()[0])
        posted_date = now - timedelta(days=days_ago)
        if posted_date > now - timedelta(days=1):
            return True
    return False

def scrape_indeed():
    try:
        url = 'https://in.indeed.com/jobs?q=software+engineer&fromage=1'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        print(f"Scraper accessed URL: {url}")
        soup = BeautifulSoup(response.content, 'html.parser')

        jobs = soup.find_all('div', class_='job_seen_beacon')

        if not jobs:
            print("No job listings found.")
            return

        for job in jobs:
            title = job.find('span', id=lambda x: x and 'jobTitle' in x)
            company = job.find('span', class_='css-63koeb eu4oa1w0')
            location = job.find('div', class_='css-1p0sjhy eu4oa1w0')
            description = job.find('li')
            date_posted = job.find('span', class_='css-qvloho eu4oa1w0')

            if title and company and location and description and date_posted:
                title_text = title.text.strip()
                company_text = company.text.strip()
                location_text = location.text.strip()
                description_text = description.text.strip()
                date_posted_text = date_posted.text.strip()

                if is_recent_job(date_posted_text):
                    if not Job.objects.filter(title=title_text, company=company_text).exists():
                        Job.objects.create(
                            title=title_text,
                            company=company_text,
                            location=location_text,
                            description=description_text,
                            date_posted=datetime.now()
                        )
                        print(f'New job added: {title_text}')
                    else:
                        print(f'Job already exists: {title_text}')
                else:
                    print(f'Job not recent enough: {title_text}')
            else:
                print("Incomplete job data found, skipping entry.")
    except Exception as e:
        print(f'Error scraping Indeed: {str(e)}')

if __name__ == '__main__':
    while True:
        scrape_indeed()
        print("Sleeping for 1 second...")
        time.sleep(1)
