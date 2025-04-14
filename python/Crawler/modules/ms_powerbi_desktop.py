from bs4 import BeautifulSoup
import urllib
import json # parse script output of download page to get a json object
import datetime
import requests                 # for getting http ressources
import re                       #import for filtering Links via RegExp
from datetime import date       # for generating dates in JSON
import logging # for logging output
import settings # import for global settings

################################### VARIABLES
LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=settings.LOGLEVEL)
# logging.basicConfig(level=logging.DEBUG)

downloads = list()

app_name = "PowerBI_Desktop".lower()
full_name = "Power BI Desktop"
default_architecture = 'win64'

# app_name_pbi_desktop = "PowerBI_reportserver".lower()
# full_name_pbi_desktop = "Power BI Report Server"
# default_architecture_pbi_desktop = 'win64'

app_version = 0

lang = 'de'
entry_page = 'https://www.microsoft.com/de-de/power-platform/products/power-bi/report-server'
download_page = ''
version_page = ''

################################### FUNCTIONS
def getWebSite(url):
    """
    Creating request with custom user agent string.

    @Param url: URL to catch the website from.
    """
    req = urllib.request.Request(
            url,
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
    with urllib.request.urlopen(req) as f:
        return BeautifulSoup(f.read().decode('utf-8'), 'html.parser')


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

def extract_download_link(website):
    """
    Extracting the download page as link.

    @param website: website object to parse from the download site.
    """
    return website.find_all('a', class_='btn btn--secondary')[0].get('href')

def extract_links(website):
    """
    Extract all links found in website.

    @param website: website with all links in it to find.
    """
    # here we store our found links => will be returned
    found_links = []

    # find script blocks in website, because here we can find the download links
    scripts = website.find_all('script')

    found_block = ''
    # iterating over all script blocks ...
    for script_block in scripts:
        # ... and searching for a specific text in script block (json with download links)
        if "window.__DLCDetails__" in script_block.text:
            # we cut off the variable name to get only the dict
            found_block = script_block.text[(script_block.text).find('=')+1:]
    # we load our found dict as json to operate later on it
    json_result = json.loads(found_block)

    # get the sub dict with all links
    dlc = json_result['dlcDetailsView']
    for url in dlc['downloadFile']:
        # append found link to our found_links
        found_links.append(url['url'])
    return found_links


def extract_version(website):
    """
    Extract version from dwonload page from website.

    @Param website: Website from where the version should be extracted.
    """
    version = ''
    # get section where the version information is stored
    version_info_section = website.find_all('section', class_='material-surface')

    version_div_site = BeautifulSoup(str(version_info_section), 'html.parser')
    # get all div containers in section
    version_div = version_div_site.find_all('div')

    # iterate over all div containers and check if string "Version" is contained
    for div in version_div:
        if "Version" in str(div):
            # we got the version div container and extract the version string
            version = div.find('p').text
    return version



def run():
    global downloads
    global app_version

    website_entry = getWebSite(entry_page)
    # hrefs = website.find_all('a',  attrs={'data-bi-ecn': re.compile(".*Advanced.*")})
    download_page = extract_download_link(website_entry)

    website_download = getWebSite(download_page)
    app_version = extract_version(website_download)
    links = extract_links(website_download)

    for link in links:
        if "PBIDesktop" in str(link):
            if "_x64" in str(link):
                downloads.append({"app_platform": "win64", "url_bin": link, "sig_type": None,
                    "sig_res": None, "hash_type": None,
                    "hash_res": None, "url_pub_key": None})
            else:
                downloads.append({"app_platform": "win32", "url_bin": link, "sig_type": None,
                    "sig_res": None, "hash_type": None,
                    "hash_res": None, "url_pub_key": None})
    return toJSON(downloads)

if __name__ == "__main__":
    import sys

    print(run())
