import Crawler.crawler
import Db.database
from Downloader import downloader
from Downloader.verify import verify_downloads

# crawl every module stored in modules path and get application information
application_links = Crawler.crawler.getApplications("Crawler")

Db.database.init_db()
Db.database.append_software(application_links)

# activate all software for download which was found latest
activate_download_for_latest_found()

# reset all download flags
# reset_download_flag_for_all()

#get software list which have to be downloaded
software2download = Db.database.get_url_bin_of_software_to_download()

downloader.download_software(software2download)