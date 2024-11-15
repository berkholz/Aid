import requests
from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map
import os

# from Downloader.utils import *
from Downloader.verify import verify
import urllib.parse # for parsing download url
import logging
import settings

################################### VARIABLES
LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=settings.LogLevel)

################################### FUNCTIONS
def initialize_download_directory():
    """initializes the download-folder"""
    LOGGER.info("Checking if download directory exists.")
    if not os.path.exists(settings.DOWNLOAD_PATH):
        LOGGER.info("Download directory does not exist, creating.")
        os.makedirs(settings.DOWNLOAD_PATH)
        LOGGER.info("Download directory " + settings.DOWNLOAD_PATH + " created.")
    else:
        LOGGER.info("Download directory " + settings.DOWNLOAD_PATH + " allready created.")

def get_software(link, base_path, software, version, platform):
    """downloads single software"""
    extension = link.split('?')[0].split('.')[-1]
    parsed_url = urllib.parse.urlsplit(link)
    quoted_file_name = str(parsed_url.path).split('/')[-1]
    # remove url special quoting characters, e.g. %20
    file_name = urllib.parse.unquote(quoted_file_name, encoding='utf-8', errors='replace')

    if link.split('?')[0].split('.')[-2] == 'tar':
        extension = 'tar.' + extension

    downl_dir = base_path + software + '/' + version + '/' + platform + '/'

    if not os.path.exists(downl_dir):
        os.makedirs(downl_dir, exist_ok=True)
    sv_path = downl_dir + file_name

    if os.path.exists(sv_path):
        res = verify(sv_path)
        if res is True:
            tqdm.write(f'verified download: {software} version: {version}')
            return
        else:
            tqdm.write('unverifiable Download found,')


    tqdm.write(f"Starting download of {software}, version {version}...")
    load = requests.get(link, timeout=300, stream=True)
    total = int(load.headers.get('content-length', 0))

    try:
        with open(sv_path, 'wb') as file, tqdm(
                desc=f'Downloading {software}',
                total=total,
                unit='iB',
                unit_scale=True,
                unit_divisor=2048,
                position=0,
                leave=True,
                dynamic_ncols=True
        ) as bar:
            for data in load.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)
    except Exception as e:
        print(e)
        os.remove(sv_path)

    tqdm.write(f'Downloaded {software} in version {version}: {sv_path}.')
    tqdm.write(f'staring verification of {software}')
    # if os.path.exists(sv_path):
    #     result = verify(sv_path)
    #     if not result:
    #         tqdm.write(f'verification failed, deleting {software} from path {sv_path}')
    #         os.remove(sv_path)
    #     else:
    #         tqdm.write(f'verification successful.')



def download_software(list_of_software):
    LOGGER.info("Start downloading.")
    for download in list_of_software:
        LOGGER.info(f"Downloading {download['app_name']} (Version {download['app_version']}, Arch: {download['app_platform']}) from {download['url_bin']}")
        get_software(download['url_bin'], DOWNLOAD_PATH, download['app_name'], download['app_version'] ,download['app_platform'])
    LOGGER.info("Stopping download.")

if __name__ == '__main__':
    LOGGER.info("Starting download.")
    initialize_download_directory()


