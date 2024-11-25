import urllib.request            # import for catching the website
from bs4 import BeautifulSoup    # import for parsing the website via beautiful soup 4 (https://www.crummy.com/software/BeautifulSoup/bs4/doc/).
from datetime import date        # import for last_found in JSON export
import logging                   # import lib for LOGGING
import settings                  # import global settings

################################### VARIABLES
LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=settings.LogLevel)
# logging.basicConfig(level=logging.DEBUG)

download_url = ""
app_name = "example_app".lower()
full_name = "Example App"
default_download = 'win64'
app_version = "0"

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

def to_json(d):
    """
    Export the JSON.

    @param d: Dictionary with all software informations for the downloads.
    """
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

    # here you add your code to parse the website and extract links and information

    app = {"app_platform": default_download, "url_bin": download_url, "sig_type": None, "sig_res": None,   "hash_type": None, "hash_res": None, "url_pub_key": None}
    downloads.append(app)

    return to_json(downloads)

if __name__ == "__main__":
    print(run())
