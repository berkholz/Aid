import requests
from bs4 import BeautifulSoup
import urllib
from datetime import date
from urllib.error import URLError, HTTPError

download_url = 'https://sqlitebrowser.org/dl/'
app_name = "sqlite_browser".lower()
full_name = "DB Browser for SQLite"
default_download = 'win64'
base_url = download_url.split('/')[0] + '//' + download_url.split('/')[1] + download_url.split('/')[2] + '/'


def findPlatformInURL(platform, url):
    if url.find(platform) > 0 and url.find('.asc') < 1 and url.find('sha256') < 1:
        return url


def isBinaryURL(ref, platform_string):
    return ref['href'].find(platform_string) > 0 and ref['href'].find('.asc') < 1 and ref['href'].find('sha256') < 1


def getWebSite():
    # creating request with custom user agent string
    response = requests.get(download_url).text
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
    website = getWebSite()
    tables = website.find('div', class_='article-content')
    global app_version
    # print(tables)
    for a in tables.find_all('a', href=True):
        tmp_platform = ''
        tmp_url_bin = ''
        tmp_url_asc = ''
        tmp_url_sha256 = ''
        if isBinaryURL(a, 'win64.msi'):
            tmp_url_bin = findPlatformInURL('win64.msi', a['href'])
            app_version = tmp_url_bin.split('-')[1]
            downloads.append(
                {"app_platform": "win64", "url_bin": tmp_url_bin, "sig_type": None, "sig_res": None, "hash_type": None,
                 "hash_res": None, "url_pub_key": None})

        elif isBinaryURL(a, '.AppImage'):
            # we have to find tar.gz, because it is a generic linux tar.gz package
            tmp_url_bin = findPlatformInURL('.AppImage', a['href'])
            downloads.append(
                {"app_platform": "linux", "url_bin": tmp_url_bin, "sig_type": None, "sig_res": None, "hash_type": None,
                 "hash_res": None, "url_pub_key": None})
            # print(url_base + a['href'])
    return toJSON(downloads)


if __name__ == "__main__":
    import sys

    print(run())
    # run(sys.argv[1])
