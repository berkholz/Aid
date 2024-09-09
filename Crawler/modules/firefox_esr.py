import urllib.request
from bs4 import BeautifulSoup
import urllib
from datetime import date
from urllib.error import URLError, HTTPError

from Crawler.modules.stunnel import base_url, app_name

app_name = "firefox_esr"
download_url = 'https://ftp.mozilla.org/pub/firefox/releases/'
base_url = download_url.split('/')[0] + '//' + download_url.split('/')[1] + download_url.split('/')[2] + '/'

lang = 'de'


def find_newest_esr(tables):
    versions = []
    for e in tables.find_all('a', href=True):
        if (e.text[-4:-1] == 'esr'):
            temp = e.text[:-4].split('.')
            if temp[0].isdigit():
                versions.append(temp)

    max_version = max(versions, key=lambda x: [int(i) for i in x] + [0] * (3 - len(x)))
    version = ".".join(max_version) + "esr"
    return version


def findPlatformInURL(platform, url):
    if url.find(platform) > 0 and url.find('.asc') < 1 and url.find('sha256') < 1:
        return url


def isBinaryURL(ref, platform_string):
    return ref['href'].find(platform_string) > 0 and ref['href'].find('.asc') < 1 and ref['href'].find('sha256') < 1


def getWebSite():
    # creating request with custom user agent string
    req = urllib.request.Request(
        download_url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )

    with urllib.request.urlopen(req) as f:
        return BeautifulSoup(f.read().decode('utf-8'), 'html.parser')


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

    global app_version

    # print(tables)
    app_version = find_newest_esr(tables)

    version_url = download_url + app_version + '/'
    url_asc = version_url + 'SHA256SUMS.asc'
    url_sha256 = version_url + 'SHA256SUMS'
    url_key = version_url + 'KEY'

    # win64
    tmp_url_bin = version_url + f'win64/{lang}/Firefox Setup {app_version}.exe'
    downloads.append({"app_platform": "win64", "url_bin": tmp_url_bin,"sig_type": "asc_file", "sig_res": url_asc, "hash_type": "sha256_multi",
                 "hash_res": url_sha256, "url_pub_key": url_key })

    # linux x86_64
    tmp_url_bin = version_url + f'win64/{lang}/firefox-{app_version}.tar.bz2'
    downloads.append({"app_platform": "linux", "url_bin": tmp_url_bin, "sig_type": 'asc_file', "sig_res": tmp_url_bin + ".asc", "hash_type": "sha256_multi",
                 "hash_res": url_sha256, "url_pub_key": url_key})

    return toJSON(downloads)


if __name__ == "__main__":
    import sys

    print(run())
    # run(sys.argv[1])
