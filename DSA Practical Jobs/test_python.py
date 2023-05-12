### Developed by Renato Cezar, based on the script "getting_started.ipynb" supplied by THE FORAGE
### to perform an on the job training for BRITISH AIRWAYS
### Last modification: May 12th 2023

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re as re
import datetime
from dateutil.parser import parse

base_url = "https://www.airlinequality.com/airline-reviews/british-airways"
# Set the number of pages to be scraped
pages = 20
# Set the number of registers per page
page_size = 100

parsed_content = []
lists_survey = []

# Loop to scrap content from each page:
for i in range(1, pages + 1):

    print(f"Scraping page {i}")

    # Create URL to collect links from paginated data
    url = f"{base_url}/page/{i}/?sortby=post_date%3ADesc&pagesize={page_size}"

    # Collect HTML data from this page
    response = requests.get(url)

    # Pre Parse content
    content = response.content
    pre_parsed_content = BeautifulSoup(content, 'html.parser')

    # Split the articles from Pre Parsed Content and store them in a list of lists
    #parsed_content = pre_parsed_content.find_all("article", {"itemprop": "review"})
    for article in pre_parsed_content.find_all("article", {"itemprop": "review"}):
        parsed_content.append(article)

    # Print the progress
    print(f"   ---> {len(parsed_content)} total reviews")