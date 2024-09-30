import Crawler.crawler
import Db.database
from Db.database import activate_download_for_latest_found
from Db.database import reset_download_flag_for_all
from Downloader import downloader
# from Downloader.verify import verify_downloads
import logging # import lib for LOGGING
import settings # import global settings

################################### VARIABLES
LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=settings.LogLevel)

# crawl every module stored in modules path and get application information
application_links = Crawler.crawler.getApplications("Crawler")


################################### MAIN

Db.database.init_db()
Db.database.append_software(application_links)

# activate all software for download which was found latest
activate_download_for_latest_found()

# reset all download flags
# reset_download_flag_for_all()

#get software list which have to be downloaded
software2download = Db.database.get_url_bin_of_software_to_download()

downloader.download_software(software2download)