import requests
from bs4 import BeautifulSoup
import urllib
from datetime import date
from urllib.error import URLError, HTTPError

MAX_ITER = 5
download_url = 'https://inkscape.org/release/'
app_name = "inkscape".lower()
full_name = "Inkscape"
default_download = 'win64'
base_url = download_url.split('/')[0] + '//' + download_url.split('/')[1] + download_url.split('/')[2] + '/'

def get_direct_url(url):
    """selects direct download url from sourceforge sites"""
    site = getWebSite(url)
    link = site.find('a', href=True)['href']
    return link

def findPlatformInURL(platform, url):
    if url.find(platform) > 0 and url.find('.asc') <1 and url.find('sha256') <1:
        return url

def isBinaryURL(ref, platform_string):
    return ref.find(platform_string) > 0 and ref.find('.asc') <1 and ref.find('sha256') <1

def getWebSite(url):
    """returns website as bs4 object"""
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

def direct(url):
    site = getWebSite(url)
    iter = 0
    while site.find('a', string='click here') is None and iter <= MAX_ITER:
        site = getWebSite(url)
    file = base_url + site.find('a',string='click here')['href']
    sig = site.find('a', string='sig')['href']
    return file, sig


def run():
    downloads = list()
    website = getWebSite(download_url)
    iter = 0
    while (website is None or website.find('li', class_='download') is None) and iter <= MAX_ITER:
        website = getWebSite(download_url)
    link_tar = website.find('li', class_='download').find('a')['href']
    # print(link_tar)
    link_win = "/".join(link_tar.split('/')[1:3])+"/windows/64-bit/msi/dl"
    # print(link_win)

    global app_version

    if isBinaryURL(link_win, '/windows/64-bit/msi/'):
        tmp_url_bin = base_url + findPlatformInURL('/windows/64-bit/msi/', link_win)
        # print(tmp_url_bin)
        app_version = tmp_url_bin.split('/')[4].split('-')[1]
        file, sha = direct(tmp_url_bin)
        downloads.append({"app_platform": "win64", "url_bin": file,"sig_type": None, "sig_res": None, "hash_type": 'sha256_single',
                 "hash_res": sha, "url_pub_key": None})

    if isBinaryURL(link_tar, '/source/archive/xz'):
        tmp_url_bin = base_url + findPlatformInURL('/source/archive/xz', link_tar)
        file, sig = direct(tmp_url_bin)
        downloads.append({"app_platform": "linux", "url_bin": file,"sig_type": 'sig_file', "sig_res": sig, "hash_type": None,
                 "hash_res": None, "url_pub_key": 'https://inkscape.org/~MarcJeanmougin/gpg/'})


    return toJSON(downloads)

if __name__ == "__main__":
    import sys
    print(run())
    #run(sys.argv[1])
