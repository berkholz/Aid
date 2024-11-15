from threading import local
from turtle import down
from wsgiref.simple_server import software_version
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


def download_file(url, local_filename):
    """
    Function to download a single file from URL. It is called from download_software()

    @param url: url that should be downloaded
    @param local_filename: save download as local_filename
    """
    # download file from url
    load = requests.get(url, timeout=300, stream=True)

    # get file size for progress bar
    total = int(load.headers.get('content-length', 0))

    try:
    # show progress bar, see tqdm
        with open(local_filename, 'wb') as file, tqdm(
                desc=f"Downloading {url}",
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
        LOGGER.error(e)
        os.remove(local_filename)


def download_software(software_download, base_path):
    """
    Function for downloading a single software package.
    It is called by function download().

    @param software_download: dictionary with app_name, app_version and app_plattform
    @param base_path: directory of the path where download is saved
    """
    extension = software_download['url_bin'].split('?')[0].split('.')[-1]
    parsed_url = urllib.parse.urlsplit(software_download['url_bin'])
    quoted_file_name = str(parsed_url.path).split('/')[-1]

    # remove url special quoting characters, e.g. %20
    file_name = urllib.parse.unquote(quoted_file_name, encoding='utf-8', errors='replace')

    # setting download path with <app_name>/<app_version>/<app_platform>/
    download_dir = base_path + software_download['app_name'] + '/' + software_download['app_version'] + '/' + software_download['app_platform'] + '/'

    # check if download path exísts, if not create directory structure
    if not os.path.exists(download_dir):
        os.makedirs(download_dir, exist_ok=True)

    if not os.path.exists(download_dir + file_name):
        LOGGER.info(f"Downloading {software_download['app_name']} (Version {software_download['app_version']}, Arch: {software_download['app_platform']}) from {software_download['url_bin']}")
        download_file(software_download['url_bin'], download_dir + file_name)
        LOGGER.info("File saved to: " + download_dir + file_name)
    else:
        LOGGER.info("File " + download_dir + file_name + " allready exists. Skipping donwload.")


def verify_signature(software_download, base_path):
#def verify(path):
    """initiates verification for a specific file"""
    LOGGER.info("Verifing signature of " + software_download['app_name'])

    # file_name = path.split('/')[-1]
    # platform = path.split('/')[-2].split('-')[0]
    # software = file_name.split('-')[0]
    # i = -1
    # if file_name.split('.')[-2] == 'tar':
    #     i = -2
    # software_version = ".".join(file_name.split('-')[1].split('.')[:i])

    software_version = software_download['app_version']
    software_name = software_download['app_name']
    # # we get our verification source
    # res = get_checksum_link(platform, software, software_version)
    LOGGER.info("checksum link: " + software_download['sig_res'])
    if software_download['sig_res'] is None:
         tqdm.write(f'No signature for software {software_name} {software_version} found in database')
         return False

    # # we start verifying checksums
    # hash_verify_status = verify_hash(path, software, res)

    # # and the continue with signatures
    # sig_verify_status = verify_signature(path, res)

    # # check for failed verification
    # if hash_verify_status == False or sig_verify_status == False:
    #     return False
    # else:
    #     return True

    # if os.path.exists():
    #     result = verify(sv_path)
    #     if not result:
    #         tqdm.write(f'verification failed, deleting {software} from path {sv_path}')
    #         os.remove(sv_path)
    #     else:
    #         tqdm.write(f'verification successful.')


def download(list_of_software):
    """
    Function for downloading a list of software. It triggers the function download_software().

    @param list_of_software: List of dictionaries of software packages.
    """
    LOGGER.info("Initiating download.")
    for download in list_of_software:
        download_software(download, settings.DOWNLOAD_PATH)
    LOGGER.info("Finishing download.")

if __name__ == '__main__':
    LOGGER.info("Starting download.")
    initialize_download_directory()


