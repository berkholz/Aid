import urllib.request
from bs4 import BeautifulSoup
import urllib
from datetime import date
from urllib.error import URLError, HTTPError
import json

api_url = 'https://rdc.adobe.io/reader/products?lang={lang}&site=enterprise&os={os}&preInstalled=&country=DE&nativeOs={os}&api_key=dc-get-adobereader-cdn'
api_link_url = 'https://rdc.adobe.io/reader/downloadUrl?name={name}&nativeOs={os}&os={os}&site=enterprise&lang={lang}&country={country}&api_key=dc-get-adobereader-cdn'

app_name = "adobe".lower()
full_name = "Adobe Reader"
default_download = 'win64'

def findPlatformInURL(platform, url):
    if url.find(platform) > 0 and url.find('.asc') < 1 and url.find('sha256') < 1:
        return url


def isBinaryURL(ref, platform_string):
    return ref['href'].find(platform_string) > 0 and ref['href'].find('.asc') < 1 and ref['href'].find('sha256') < 1


def call_api(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }

    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as f:
        data = json.loads(f.read().decode('utf-8'))
        return data


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
    # website = getWebSite()
    # tables = website.table
    global app_version
    lang = "de"
    country = "DE"
    os_list = ["Windows+10"]

    for os in os_list:

        response = call_api(api_url.format(lang=lang, os=os))
        # print(response)

        app_version = response['products']['reader'][0]['version']
        display_name = response['products']['reader'][0]['displayName']
        display_name = display_name.replace(" ", "+")

        url_response = call_api(api_link_url.format(name=display_name, os=os, country=country, lang=lang))
        # print(url_response)

        tmp_url = url_response['downloadURL']
        # print(tmp_url)
        # print(app_version)
        if (tmp_url.find('.exe') >= 0):
            # print(tmp_url)
            downloads.append(
                {"app_platform": "win64", "url_bin": tmp_url, "sig_type": None, "sig_res": None, "hash_type": None,
                 "hash_res": None, "url_pub_key": None})

        if (tmp_url.find('.apk') >= 0):
            # print(tmp_url)
            downloads.append(
                {"app_platform": "android", "url_bin": tmp_url, "sig_type": None, "sig_res": None, "hash_type": None,
                 "hash_res": None, "url_pub_key": None})

    return toJSON(downloads)


if __name__ == "__main__":
    import sys

    print(run())
    # run(sys.argv[1])
