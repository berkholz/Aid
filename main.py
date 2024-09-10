import Crawler.crawler
import Db
import Db.database
from downloader import downloader
from packager.verify import verify_dir


# crawl every module stored in modules path and get application information
application_links = Crawler.crawler.getApplications("Crawler")

Db.database.init_db()
Db.database.append_software(application_links)

down_path = downloader.download('win64')
check = verify_dir(down_path)
