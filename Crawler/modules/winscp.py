import urllib.request
from bs4 import BeautifulSoup
import urllib
from datetime import date
import requests

download_url = 'https://winscp.net/eng/download.php'
app_name = "winscp".lower()
full_name = "WinSCP"
default_download = 'win64'
base_url = download_url.split('/')[0] + '//' + download_url.split('/')[1] + download_url.split('/')[2] + '/'
app_version = 0


def findPlatformInURL(platform, url):
    if url.find(platform) > 0 and url.find('.gpg') < 1:
        return url


def isBinaryURL(ref, platform_string):
    return ref['href'].find(platform_string) > 0 and ref['href'].find('.gpg') < 1


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
    # print(website)
    global app_version

    downloadsite_url = base_url + website.find('a', href=True, class_='btn-primary')['href']
    downloadsite = getWebSite(downloadsite_url)

    links = downloadsite.find_all('a', href=True, attrs={'rel': 'nofollow'})

    tmp_platform = ''
    tmp_url_bin = ''
    tmp_url_asc = ''
    tmp_url_sha256 = ''
    for a in links:
        if isBinaryURL(a, '.exe') and a.text.find("Direct") >= 0:
            tmp_url_bin = findPlatformInURL('.exe', a['href'])
            app_version = tmp_url_bin.split('-')[1]
            downloads.append({"app_platform": "win64", "url_bin": tmp_url_bin,"sig_type": None, "sig_res": None, "hash_type": None,
                 "hash_res": None, "url_pub_key": None})

    return toJSON(downloads)


if __name__ == "__main__":
    import sys

    print(run())
    # run(sys.argv[1])
