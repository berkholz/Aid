import urllib.request
from bs4 import BeautifulSoup
import urllib
from datetime import date
import requests

download_url = 'https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html'
app_name = "putty".lower()
full_name = "Putty"
default_download = 'win64'
base_url = download_url.split('/')[0] + '//' + download_url.split('/')[1] + download_url.split('/')[2] + '/'
app_version = 0
pub_key= 'https://www.chiark.greenend.org.uk/~sgtatham/putty/keys/release-2023.asc'


def findPlatformInURL(platform, url):
    if url.find(platform) > 0 and url.find('.gpg') < 1:
        return url


def isBinaryURL(ref, platform_string):
    return ref['href'].find(platform_string) > 0 and ref['href'].find('.gpg') < 1


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
    tables = website.find('div', class_='downloadbottom downloadlatestbotcolour')
    # print (tables)
    global app_version

    for span in tables.find_all('span'):
        # print(span)
        for a in span.find_all('a', href=True):
            # print(f"\t{a}")
            tmp_platform = ''
            tmp_url_bin = ''
            tmp_url_asc = ''
            tmp_url_sha256 = ''
            if a.find('faq.html'):
                continue

            elif isBinaryURL(a, '64bit'):
                tmp_url_bin = findPlatformInURL('64bit', a['href'])
                app_version = tmp_url_bin.split('-')[2]
                downloads.append({"app_platform": "win64", "url_bin": tmp_url_bin, "sig_type": 'gpg_file',
                                  "sig_res": tmp_url_bin + '.gpg', "hash_type": None, "hash_res": None,
                                  "url_pub_key": pub_key})

            elif isBinaryURL(a, 'tar.gz'):
                # we have to find tar.gz, because it is a generic linux tar.gz package
                tmp_url_bin = findPlatformInURL('tar.gz', a['href'])
                downloads.append({"app_platform": "linux", "url_bin": tmp_url_bin, "sig_type": 'gpg_file',
                                  "sig_res": tmp_url_bin + '.gpg', "hash_type": None, "hash_res": None,
                                  "url_pub_key": pub_key})
                # print(url_base + a['href'])
    return toJSON(downloads)


if __name__ == "__main__":
    import sys

    print(run())
    # run(sys.argv[1])
