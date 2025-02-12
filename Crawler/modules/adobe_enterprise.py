from urllib import request
from bs4 import BeautifulSoup
import urllib
import datetime
import requests                 # for getting http ressources
import re                       #import for filtering Links via RegExp
from datetime import date
import logging

import settings # import global settings


################################### VARIABLES
LOGGER = logging.getLogger(__name__)
# logging.basicConfig(level=settings.LOGLEVEL)
logging.basicConfig(level=logging.DEBUG)

downloads = list()
download_url = ""
app_name = "adobe_enterprise".lower()
full_name = "Adobe Reader Enterprise"
default_architecture = 'win32'
app_version = 0

################################### FUNCTIONS
def get_website_as_request(url):
    """
    Function to get the website (url).

    @Param url: url from the website to catch.
    @return: Request object from website with url.
    """
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
    try:
        req = requests.get(url, headers=headers, timeout=settings.CRAWLER_MODULE_REQUEST_TIMEOUT)
    except requests.exceptions.RequestException as e:
        LOGGER.error(e)
        req = None
    return req

def get_month_name_by_number(month_number):
    """
    Function to convert a month number to a 3 letter month name.

    @param month_number: Number of month that should be converted to a 3 letter month name.
    """
    month = datetime.datetime(datetime.datetime.now().year, month_number, 1)
    if month_number == 6 or month_number == 7:
        month_name = month.strftime("%B").lower()[0:4]
    else:
        month_name = month.strftime("%B").lower()[0:3]
    return month_name

def build_download_link():
    """Generate the url to the download page."""
    base_url = "https://www.adobe.com/devnet-docs/acrobatetk/tools/ReleaseNotesDC/continuous/dccontinuous"
    year = str(datetime.datetime.now().year)
    month = datetime.datetime.now()
    month_number = datetime.datetime.now().month
    month_name = ""

    try:
        request = get_website_as_request(base_url + get_month_name_by_number(month_number) + year + ".html")
    except requests.exceptions.RequestException as e:
        LOGGER.exception(e)

    # check if
    if request == None:
        destination_url = base_url + get_month_name_by_number(month_number - 1) + year + ".html"
    else:
        if request.status_code == 404:
            destination_url = base_url + get_month_name_by_number(month_number - 1) + year + ".html"
        else:
            # return link with month and year
            destination_url = base_url + get_month_name_by_number(month_number) + year + ".html"
    return destination_url

def get_website(download_url):
    """
    creating request with custom user agent string

    @param download_url:
    """
    response = requests.get(download_url).text
    return BeautifulSoup(response, 'html.parser')

def toJSON(d):
    """convert result as JSON"""
    json_result = {
        "app_name": app_name,
        "full_name": full_name,
        "default_download": default_architecture,
        "app_version": app_version,
        "downloads": d,
        "last_found": date.today().isoformat(),
        "last_download": "0000-00-00",
    }
    return json_result

def extract_links(table, architecture):
    """Extract download url for the given architecture from the HTML table from the download page."""
    for link in table.find_all('a'):
        if re.search('.*AcroRdrDC[0-9A-Za-z]+(\\.msp|_MUI\\.dmg)$', link.get('href')) != None:
            download_link = link.get('href')
            return {"app_platform": architecture, "url_bin": download_link, "sig_type": None, "sig_res": None, "hash_type": None, "hash_res": None, "url_pub_key": None}

def extract_version(download_website):
    """Extract version from dwonload page from website."""
    return download_website.h1.text.split(' ')[0]

def run():
    global downloads
    global app_version

    website = get_website(build_download_link())

    app_version = extract_version(website)

    # get all tables with downloads of any architecture
    tables = website.find_all('table')

    # iterate over tables by architecture
    for table in tables:
        if table['id'] == 'id1': # win32
            downloads.append(extract_links(table, "win32"))
        if table['id'] == 'id2': # win64
            downloads.append(extract_links(table, "win64"))
        if table['id'] == 'id3': # mac
            downloads.append(extract_links(table, "mac"))
    return toJSON(downloads)

if __name__ == "__main__":
    print(run())
