import Crawler.crawler
import Db.database
from Downloader import downloader
from Downloader.verify import verify_downloads

# crawl every module stored in modules path and get application information
application_links = Crawler.crawler.getApplications("Crawler")

Db.database.init_db()
Db.database.append_software(application_links)

# downloader.download('win64')
