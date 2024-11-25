#############################################################################
#                                                                           #
# This Crawler module is the simplest form to download a software.          #
# By defining the variables with concrete urls and application informations #
# you can add software packages for donwloading to the Crawler.             #
#############################################################################

from ast import List
from email.mime import application
import urllib.request
from bs4 import BeautifulSoup
import urllib
from datetime import date
import logging # import lib for LOGGING
# import settings # import global settings

################################### VARIABLES
LOGGER = logging.getLogger(__name__)
# logging.basicConfig(level=settings.LogLevel)
logging.basicConfig(level=logging.DEBUG)

download_url = 'https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-12.8.0-amd64-netinst.iso'
app_name = "debian".lower()
full_name = "Debian Installation media (amd64)"
default_download = 'linux'
app_version = "12.8.0"

################################### FUNCTIONS
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
    application = {"app_platform": default_download, "url_bin": download_url, "sig_type": None, "sig_res": None, "hash_type": None, "hash_res": None, "url_pub_key": None}
    LOGGER.debug("Adding application: " + str(application))
    downloads.append(application)
    return toJSON(downloads)

if __name__ == "__main__":
    import sys
    print(run())
