from platform import win32_ver
from textwrap import shorten
from tkinter import NO
import urllib.request
from bs4 import BeautifulSoup
import urllib
from datetime import date # for getting last_found date
import requests # for requesting HTTP ressources

import urllib.parse # for parsing download url
import logging # for logging
import settings # import global settings
import re # import for parsing version string


################################### VARIABLES
LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=settings.LOGLEVEL)
# logging.basicConfig(level=logging.DEBUG)

download_url = 'https://www.gimp.org/downloads/'
app_name = "gimp".lower()
full_name = "Gnu Image Manipulation Program"
default_download = 'win64'
base_url_hashes = "https://download.gimp.org/gimp/"
app_version = 0

################################### FUNCTIONS
def isBinaryURL(ref, platform_string):
    return ref.find(platform_string) > 0 and ref.find('.asc') < 1 and ref.find('sha256') < 1

def get_hash_file(version, platform,  base_url):
    shortend_version = version.split('.')
    del shortend_version[len(shortend_version)-1]
    concatenated_shortend_version = ".".join(shortend_version)
    return base_url + "v" + concatenated_shortend_version + "/" + platform + "/SHA256SUMS"


def getWebSite(url):
    # creating request with custom user agent string
    response = requests.get(url).text
    return BeautifulSoup(response, 'html.parser')


def toJSON(d):

    json_result = {
        "app_name": app_name,
        "full_name": full_name,
        "default_download": default_download,
        "app_version": app_version,
        "downloads": d,
        "last_found": date.today().isoformat(),
        "last_download": "0000-00-00",
    }
    return json_result


def run():
    global app_version
    downloads = list()

    website = getWebSite(download_url)

    # windows links
    win = website.find(id='win')

    win_link = "https:" + win.find('a', id="win-download-link", href=True)['href']
    LOGGER.debug("extracted link:" + win_link)

    app_version = re.findall("[0-9]+\.[0-9]+\.[0-9]+", win.find('a', id="win-download-link", href=True).text)[0]
    LOGGER.debug("extracted version: " + app_version)

    if isBinaryURL(win_link, '.exe'):
        downloads.append(
            {"app_platform": "win64", "url_bin": win_link, "sig_type": None, "sig_res": None, "hash_type": "sha256_multi",
             "hash_res": get_hash_file(app_version, "windows", base_url_hashes), "url_pub_key": None})

    # mac links
    for mac_arch in ['mac-arm64-buttons','mac-x86_64-buttons']:
        # find elements for specific mac architecture
        macosx = website.find(id=mac_arch)
        # get the hrefs
        macosx_links = macosx.find_all('a')
        # aprse all links
        for link in macosx_links:
            ahref = link.get('href')
            # we want the direct download, so no torrent
            if (re.search("\.torrent", ahref) == None):
                mac_link = "https:" + ahref
                # extracting the version
                app_version = re.findall("[0-9]+\.[0-9]+\.[0-9]+", link.text)[0]
                # setting the arch for the db entry
                if mac_arch == "mac-arm64-buttons":
                    app_platform = "mac_arm"
                else:
                    app_platform = "mac"
                downloads.append(
                    {"app_platform": app_platform, "url_bin": mac_link, "sig_type": None, "sig_res": None, "hash_type": "sha256_multi",
                    "hash_res": get_hash_file(app_version, "macos", base_url_hashes), "url_pub_key": None})
    return toJSON(downloads)


if __name__ == "__main__":
    print(run())
