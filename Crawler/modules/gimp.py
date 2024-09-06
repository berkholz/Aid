import urllib.request
from bs4 import BeautifulSoup
import urllib
from datetime import date
import requests

download_url = 'https://www.gimp.org/downloads/'
app_name = "gimp".lower()
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
    # print (website)
    win = website.find(id = 'win')
    global app_version
    # print(newest_table)
    win_link = win.find('a',id="win-download-link",href=True)['href']
    win_sha256 = win.find('kbd').text
    # print (win_link," ",win_sha256)


    if isBinaryURL(win_link, '.exe'):
        tmp_url_bin = ('https:' + win_link)
        # print(tmp_url_bin)
        app_version = tmp_url_bin.split('/')[4]
        downloads.append({"app_platform": "win64", "url_bin": tmp_url_bin, "url_asc": None,
                          "url_sha256": win_sha256})


    lin = website.find(id = 'linux')
    lin_link = lin.find('a',href=True)['href']
    # print(lin_link)



    if isBinaryURL(lin_link, '.flatpakref'):
        # we have to find tar.gz, because it is a generic linux tar.gz package
        tmp_url_bin = findPlatformInURL('.flatpakref', lin_link)
        downloads.append({"app_platform": "linux", "url_bin": tmp_url_bin, "url_asc": None,
                          "url_sha256": None})
        # print(url_base + a['href'])
    return toJSON(downloads)


if __name__ == "__main__":
    import sys

    print(run())
    # run(sys.argv[1])
