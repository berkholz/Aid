import urllib.request
from bs4 import BeautifulSoup
import urllib
from datetime import date
import requests

download_url = 'https://learn.microsoft.com/de-de/sysinternals/downloads/'
app_name = "sysinternal_Utilities".lower()
base_url = download_url.split('/')[0] + '//' + download_url.split('/')[1] + download_url.split('/')[2] + '/'
app_version = 0


def findPlatformInURL(platform, url):
    if url.find(platform) > 0 and url.find('.asc') < 1 and url.find('sha256') < 1:
        return url


def isBinaryURL(ref, platform_string):
    return ref.find(platform_string) > 0 and ref.find('.asc') < 1 and ref.find('sha256') < 1


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
    # print(website)
    complete = website.find('a', string="Sysinternals Suite", href=True)['href']

    global app_version
    app_version = website.find('time').text

    if isBinaryURL(complete, '.zip'):
        tmp_url_bin = base_url + findPlatformInURL('.zip', complete)

        downloads.append({"app_platform": "win64", "url_bin": tmp_url_bin, "url_asc": None,
                          "url_sha256": None})

    return toJSON(downloads)


if __name__ == "__main__":
    import sys

    print(run())
    # run(sys.argv[1])
