from sys import setprofile
import Crawler.crawler
import Db.database
from Db.database import activate_download_for_latest_found
from Db.database import reset_download_flag_for_all
import Downloader.downloader
from Downloader.verify import import_key_from_url, verify
import logging # import lib for LOGGING
import settings # import global settings
import Verifier.verifier

################################### VARIABLES
# LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=settings.LOGLEVEL)


################################### MAIN
# crawl every module stored in modules path and get application information
applications = Crawler.crawler.getApplications("Crawler")

Db.database.init_db()
Db.database.append_software(applications)

# activate all software for download which was found latest
activate_download_for_latest_found()

# reset all download flags
# reset_download_flag_for_all()

#get software list which have to be downloaded
software2download = Db.database.get_url_bin_of_software_to_download()

#import vendor keys for verifing
# Verifier.verifier.import_keys(software2download)

Downloader.downloader.download(software2download)

# Verifier.verifier.verify(software2download)
