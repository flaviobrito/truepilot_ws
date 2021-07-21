### Trustpilot data scraping module
## Imports
import os
from pathlib import Path
import math
import csv
import time
import json
import requests
import lxml.html as html
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from common.config import settings
import logging
logging.info(f"Settings are:{settings}")

# Trustpilot review page
URL = settings['url']
REVIEW_SITE = settings['review_site']
REVIEW_PAGE = URL + REVIEW_SITE
REVIEW_SITE_FILE = REVIEW_SITE.replace('.', '_')
# Data file to save to
DATA_FILE = 'data_' + REVIEW_SITE_FILE + '.csv'

# Folder to save our cleaned data for analyse step
DATA_OUTFOLDER = settings['data_outfolder']
DATA_OUTFOLDER = os.path.join('data', DATA_OUTFOLDER)

def make_dirs(directories):
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

def main():

    make_dirs([DATA_OUTFOLDER])

    # Trustpilot default
    resultsPerPage = 20

    print('Scraper set for ' + REVIEW_PAGE + ' - saving result to ' + DATA_FILE)
    ## Count amount of pages to scrape

    # Get page, skipping HTTPS as it gives certificate errors
    page = requests.get(REVIEW_PAGE, verify=False)
    tree = html.fromstring(page.content)

    # Total amount of ratings
    ratingCount = tree.xpath('//span[@class="headline__review-count"]')
    ratingCount = int(ratingCount[0].text.replace(',', ''))

    tot_chunks = 20

    # With sleepTime seconds between every page request
    throttle = True
    sleepTime = 2

    # Total pages to scrape
    pages = math.ceil(ratingCount / resultsPerPage)
    print('Found total of ' + str(pages) + ' pages to scrape')

    with open(os.path.join(DATA_OUTFOLDER, DATA_FILE), 'w', newline='', encoding='utf8') as csvfile:

        # Tab delimited to allow for special characters
        datawriter = csv.writer(csvfile, delimiter='\t')
        print('Processing..')
        for i in range(1, pages + 1):

            # Sleep if throttle enabled
            if (throttle): time.sleep(sleepTime)

            page = requests.get(REVIEW_PAGE + '?page=' + str(i))
            tree = html.fromstring(page.content)

            # Each item below scrapes a pages review titles, bodies and ratings
            script_bodies = tree.xpath("//script[starts-with(@data-initial-state, 'review-info')]")
            for idx, elem in enumerate(script_bodies):
                curr_item = json.loads(elem.text_content())

                # Progress counting, outputs for every processed chunk
                reviewNumber = idx + 20 * (i - 1) + 1
                chunk = int(ratingCount / tot_chunks)
                if (reviewNumber % chunk == 0):
                    print('Processed ' + str(reviewNumber) + '/' + str(ratingCount) + ' ratings')

                title = curr_item["reviewHeader"]
                body = curr_item["reviewBody"]
                rating = curr_item["stars"]
                customer = curr_item["consumerName"]

                datawriter.writerow([title, body, rating, customer])

        print('Processed ' + str(ratingCount) + '/' + str(ratingCount) + ' ratings.. Finished!')


if __name__ == '__main__':
    main()
