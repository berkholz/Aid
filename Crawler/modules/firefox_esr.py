import urllib.request
from bs4 import BeautifulSoup
import urllib
from datetime import date
from urllib.error import URLError, HTTPError
import logging # for logging output
import settings # import for global settings

################################### VARIABLES
LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=settings.LOGLEVEL)

app_name = "firefox_esr"
full_name = "Firefox ESR"
default_download = 'win64'
app_version = '0'

lang = 'de'
download_page = 'https://www.mozilla.org/de/firefox/all/desktop-esr/' + default_download + '-msi/' + lang + '/'
version_page = 'https://www.mozilla.org/de/firefox/organizations/notes/'
parsed_url = urllib.parse.urlsplit(download_page)
base_url = parsed_url.scheme + parsed_url.netloc + parsed_url.path
hash_sig_base_url = 'http://releases.mozilla.org/pub/mozilla.org/firefox/releases/'

################################### FUNCTIONS

def getWebSite(url):
    # creating request with custom user agent string
    req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )
    with urllib.request.urlopen(req) as f:
        return BeautifulSoup(f.read().decode('utf-8'), 'html.parser')

def extract_version(url):
    """
    Function for extracting the version string of the website.

    @param url: Website from where the version string is extracted.
    """
    # here we catch the complete download site for extracting the version
    website = getWebSite(url)

    # we search for all links with class c-download-button
    version_element = website.find_all('span', 'c-release-version')
    LOGGER.debug("HTML element with version string: %s", str(version_element))
    # we extract the version of the download, if you want to get the latest remove "- 1" in brackets
    return version_element[0].get_text()# + 'esr'

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
    global app_version
    downloads = list()

    app_version = extract_version(version_page)

    # we set the base url for the download
    download_base_url = 'https://download-installer.cdn.mozilla.net/pub/firefox/releases/' + app_version + '/'

    version_url = hash_sig_base_url + app_version + '/'
    url_asc = version_url + 'SHA256SUMS.asc'
    url_sha256 = version_url + 'SHA256SUMS'
    url_key = version_url + 'KEY'

    # win32
    tmp_architecture = 'win32'
    tmp_url = download_base_url + tmp_architecture + '/' + lang +'/Firefox%20Setup%20' + app_version + '.msi'
    downloads.append({"app_platform": tmp_architecture, "url_bin": tmp_url, "sig_type": "asc_file", "sig_res": url_asc, "hash_type": "sha256_multi", "hash_res": url_sha256, "url_pub_key": url_key })

    # win64
    tmp_architecture = 'win64'
    tmp_url = download_base_url + tmp_architecture + '/' + lang +'/Firefox%20Setup%20' + app_version + '.msi'
    downloads.append({"app_platform": tmp_architecture, "url_bin": tmp_url, "sig_type": "asc_file", "sig_res": url_asc, "hash_type": "sha256_multi", "hash_res": url_sha256, "url_pub_key": url_key })

    # linux
    tmp_architecture = 'linux-x86_64'
    tmp_url = download_base_url + tmp_architecture + '/' + lang +'/Firefox%20Setup%20' + app_version + '.msi'
    downloads.append({"app_platform": tmp_architecture, "url_bin": tmp_url, "sig_type": "asc_file", "sig_res": url_asc, "hash_type": "sha256_multi", "hash_res": url_sha256, "url_pub_key": url_key })

    return toJSON(downloads)


if __name__ == "__main__":
    print(run())
