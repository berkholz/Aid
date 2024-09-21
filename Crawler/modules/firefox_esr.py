import urllib.request
from bs4 import BeautifulSoup
import urllib
from datetime import date
from urllib.error import URLError, HTTPError

app_name = "firefox_esr"
full_name = "Firefox ESR"
architecture = 'win64'

lang = 'de'
download_page = 'https://www.mozilla.org/de/firefox/all/desktop-esr/' + architecture + '-msi/' + lang + '/'
parsed_url = urllib.parse.urlsplit(download_page)
base_url = parsed_url.scheme + parsed_url.netloc + parsed_url.path
download_url = ''
hash_sig_base_url = 'http://releases.mozilla.org/pub/mozilla.org/firefox/releases/'

def getWebSite():
    # creating request with custom user agent string
    req = urllib.request.Request(
        download_page,
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
        "default_download": architecture,
        "app_version": app_version,
        "downloads": d,
        "last_found": date.today().isoformat(),
        "last_download": "0000-00-00",
    }
    return json_result


def run():
    downloads = list()
    global app_version
    global download_url
    global architecture

    # here we catch the complete download site
    website = getWebSite()

    # we search for all links with class c-download-button
    ahrefs = website.find_all('a', 'c-download-button')

    # we extract the version of the download, if you want to get the latest remove "- 1" in brackets
    app_version = ahrefs[len(ahrefs) - 1].text.split()[0] + 'esr'

    # we extract the download url
    download_base_url = 'https://download-installer.cdn.mozilla.net/pub/firefox/releases/' + app_version + '/'

    version_url = hash_sig_base_url + app_version + '/'
    url_asc = version_url + 'SHA256SUMS.asc'
    url_sha256 = version_url + 'SHA256SUMS'
    url_key = version_url + 'KEY'

    # win32
    architecture = 'win32'
    tmp_url = download_base_url + architecture + '/' + lang +'/Firefox%20Setup%20' + app_version + '.msi'
    downloads.append({"app_platform": architecture, "url_bin": tmp_url, "sig_type": "asc_file", "sig_res": url_asc, "hash_type": "sha256_multi", "hash_res": url_sha256, "url_pub_key": url_key })

    # win64
    architecture = 'win64'
    tmp_url = download_base_url + architecture + '/' + lang +'/Firefox%20Setup%20' + app_version + '.msi'
    downloads.append({"app_platform": architecture, "url_bin": tmp_url, "sig_type": "asc_file", "sig_res": url_asc, "hash_type": "sha256_multi", "hash_res": url_sha256, "url_pub_key": url_key })

    # linux
    architecture = 'linux-x86_64'
    tmp_url = download_base_url + architecture + '/' + lang +'/Firefox%20Setup%20' + app_version + '.msi'
    downloads.append({"app_platform": architecture, "url_bin": tmp_url, "sig_type": "asc_file", "sig_res": url_asc, "hash_type": "sha256_multi", "hash_res": url_sha256, "url_pub_key": url_key })

    return toJSON(downloads)


if __name__ == "__main__":
    import sys

    print(run())
    # run(sys.argv[1])
