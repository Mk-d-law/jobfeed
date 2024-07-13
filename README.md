# jobfeed_project

## Project Overview

The jobfeed_project is a Django application developed to generate an XML job feed compatible with Indeed's requirements. It integrates job scraping from Indeed, updates the feed automatically with new job postings, and provides an XML feed endpoint for integration with other systems.

## Features

- Generates an XML job feed from Django database.
- Scrapes job listings from Indeed and updates the database automatically.
- XML feed adheres to Indeed's XML feed specifications.
- Provides real-time updates as new jobs are posted.

## Technologies Used

- Python 3.10
- Django 5.0.2
- SQLite (for local development)


## Setup Instructions

### Prerequisites

- Python 3.10 installed on your system
- Ensure pip is up-to-date (`pip install --upgrade pip`)

### Installation

1. Clone the repository:
```bash
   git clone https://github.com/Mk-d-law/jobfeed
   cd jobfeed_project
```
   
2.Apply database migrations:
```bash
   python manage.py migrate
```
3.run scraper.py:
```bash
  python scraper.py
```

4.run django server:
```bash
  python manage.py runserver
```




  




