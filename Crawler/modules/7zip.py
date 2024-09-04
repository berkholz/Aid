import urllib.request
from bs4 import BeautifulSoup
import urllib
from datetime import date
import requests

download_url = 'https://www.7-zip.org/download.html'
app_name = "7zip".lower()
base_url = download_url.split('/')[0] + '//' + download_url.split('/')[1] + download_url.split('/')[2] + '/'
app_version = 0


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
        "app_version": app_version,
        "downloads": d,
        "last_found": date.today().isoformat(),
        "last_download": "0000-00-00"
    }
    return json_result


def run():
    downloads = list()
    website = getWebSite()
    tables = website.table
    newest_table = tables.find_all('table')[3]
    global app_version
    # print(newest_table)
    for a in newest_table.find_all('a', href=True):
        tmp_platform = ''
        tmp_url_bin = ''
        tmp_url_asc = ''
        tmp_url_sha256 = ''

        if isBinaryURL(a, 'x64.exe'):
            tmp_url_bin = base_url + findPlatformInURL('x64.exe', a['href'])
            app_version = tmp_url_bin.split('/')[-1].split('-')[0][2:]
            downloads.append({"app_platform": "win64", "url_bin": tmp_url_bin, "url_asc": None,
                              "url_sha256": None})

        elif isBinaryURL(a, 'linux-x64.tar.xz'):
            # we have to find tar.gz, because it is a generic linux tar.gz package
            tmp_url_bin = base_url + findPlatformInURL('linux-x64.tar.xz', a['href'])
            downloads.append({"app_platform": "linux", "url_bin": tmp_url_bin, "url_asc": None,
                              "url_sha256": None})
            # print(url_base + a['href'])
    return toJSON(downloads)


if __name__ == "__main__":
    import sys

    print(run())
    # run(sys.argv[1])
