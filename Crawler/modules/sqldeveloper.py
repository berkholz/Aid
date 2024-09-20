import urllib.request
from bs4 import BeautifulSoup
import urllib
from datetime import date
from urllib.error import URLError, HTTPError

download_url = 'https://www.oracle.com/database/sqldeveloper/technologies/download/'
app_name = "sqldeveloper".lower()
full_name = "SQL Developer"
default_download = 'win64'
base_url = download_url.split('/')[0] + '//' + download_url.split('/')[1] + download_url.split('/')[2] + '/'


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
    tables = website.find('table', class_='otable-w2')
    # print(tables)
    global app_version

    for row in tables.find_all('tr'):
        a = row.find('a', href=True)
        tmp_platform = ''
        tmp_url_bin = ''
        tmp_url_asc = ''
        tmp_url_sha256 = ''

        if a is None or not a.has_attr('href'):
            continue

        if isBinaryURL(a, 'x64.zip'):
            tmp_url_bin = 'https:' + findPlatformInURL('x64.zip', a['href'])
            app_version = tmp_url_bin.split('-')[1]

            sha1_element = row.find('li', string=lambda text: 'SHA1:' in text if text else False)
            sha1 = sha1_element.text.split(': ')[1]

            downloads.append(
                {"app_platform": "win64", "url_bin": tmp_url_bin, "sig_type": None, "sig_res": None,
                 "hash_type": 'sha1_string', "hash_res": sha1, "url_pub_key": None})

        elif isBinaryURL(a, 'noarch.rpm'):
            # we have to find tar.gz, because it is a generic linux tar.gz package
            tmp_url_bin = 'https:' + findPlatformInURL('noarch.rpm', a['href'])

            sha1_element = row.find('li', string=lambda text: 'SHA1:' in text if text else False)
            sha1 = sha1_element.text.split(': ')[1]

            downloads.append(
                {"app_platform": "linux", "url_bin": tmp_url_bin, "sig_type": None, "sig_res": None,
                 "hash_type": 'sha1_string', "hash_res": sha1, "url_pub_key": None})

            # print(url_base + a['href'])
    return toJSON(downloads)


if __name__ == "__main__":
    import sys

    print(run())
    # run(sys.argv[1])
