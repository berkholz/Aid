import urllib.request
from bs4 import BeautifulSoup
import urllib
from datetime import date
from urllib.error import URLError, HTTPError
import requests
from gnupg import string_types

download_url = 'https://notepad-plus-plus.org/downloads/'
app_name = "notepad++".lower()
full_name = "Notepad++"
default_download = 'win64'
base_url = download_url.split('/')[0] + '//' + download_url.split('/')[1] + download_url.split('/')[2] + '/'


def findPlatformInURL(platform, url):
    if url.find(platform) > 0 and url.find('.sig') < 1 and url.find('sha256') < 1:
        return url


def isBinaryURL(ref, platform_string):
    return ref['href'].find(platform_string) > 0 and ref['href'].find('.sig') < 1 and ref['href'].find('sha256') < 1


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
    downloads = list()
    website = getWebSite(download_url)
    main = website.find('main', id='main')
    newest = main.find('a', href=True)
    url_newest = newest['href']

    website = getWebSite(url_newest)
    tables = website.find('main', id='main').find('ul')
    tab_sha = website.find('main', id='main').find('a', href=lambda href: href and 'sha256' in href)
    # print(tables)

    global app_version

    # print(tables)
    for a in tables.find_all('a', href=True):
        tmp_platform = ''
        tmp_url_bin = ''
        tmp_url_asc = ''
        tmp_url_sha256 = ''
        if isBinaryURL(a, 'x64.exe'):
            tmp_url_bin = findPlatformInURL('x64.exe', a['href'])
            tmp_url_sha256 = tab_sha['href']
            app_version = tmp_url_bin.split('/')[-2]
            downloads.append({"app_platform": "win64", "url_bin": tmp_url_bin, "sig_type": 'sig_file',
                              "sig_res": tmp_url_bin + ".sig", "hash_type": 'sha256_multi',
                              "hash_res": tmp_url_sha256, "url_pub_key": 'https://notepad-plus-plus.org/gpg/nppGpgPub.asc'})

            # print(url_base + a['href'])
    return toJSON(downloads)


if __name__ == "__main__":
    import sys

    print(run())
    # run(sys.argv[1])
