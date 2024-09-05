import requests
from bs4 import BeautifulSoup
import urllib
from datetime import date
from urllib.error import URLError, HTTPError
from Crawler import sourceforge_direct_url_helper
from Crawler.sourceforge_direct_url_helper import get_direct_url

download_url = 'https://keepass.info/download.html'
app_name = "keepass".lower()
base_url = download_url.split('/')[0] + '//' + download_url.split('/')[1] + download_url.split('/')[2] + '/'


def findPlatformInURL(platform, url):
    if url.find(platform) > 0 and url.find('.asc') <1 and url.find('sha256') <1:
        return url

def isBinaryURL(ref, platform_string):
    return ref['href'].find(platform_string) > 0 and ref['href'].find('.asc') <1 and ref['href'].find('sha256') <1

def getWebSite(url):
    # creating request with custom user agent string
    response = requests.get(url).text
    return BeautifulSoup(response, 'html.parser')


def toJSON(d):
    json_result = {
        "app_name" : app_name,
        "app_version": app_version,
        "downloads" : d,
        "last_found": date.today().isoformat(),
        "last_download": "0000-00-00"
    }
    return json_result

def run():
    downloads = list()
    website = getWebSite(download_url)
    tables = website.table.table
    global app_version
    #print(tables)
    for a in tables.find_all('a', href=True):
        #print(a)
        tmp_platform = ''
        tmp_url_bin = ''
        tmp_url_asc = ''
        tmp_url_sha256 = ''
        if isBinaryURL(a, '.exe'):
            tmp_url_bin = findPlatformInURL('.exe', a['href'])
            app_version = tmp_url_bin.split('-')[1]
            link = get_direct_url(tmp_url_bin)
            downloads.append({"app_platform": "win64", "url_bin": link, "url_asc":None, "url_sha256": None})

    return toJSON(downloads)

if __name__ == "__main__":
    import sys
    print(run())
    #run(sys.argv[1])
