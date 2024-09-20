import requests
from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map

from Db.database import get_sw_list_for_platform, get_software_link
from download.utils import *
from download.verify import verify



def path_init():
    """initializes the download-folder"""
    if not os.path.exists(DOWNLOAD_PATH):
        os.makedirs(DOWNLOAD_PATH)


def download_sw(software, app_platfom, version, path):
    """downloads single software"""

    link = get_software_link(software, app_platfom, version)

    # print (link)
    extension = link.split('?')[0].split('.')[-1]

    if link.split('?')[0].split('.')[-2] == 'tar':
        extension = 'tar.' + extension

    downl_dir = path + "/" + software + '/' + version + '/' + app_platfom + '/'

    if not os.path.exists(downl_dir):
        os.makedirs(downl_dir, exist_ok=True)
    sv_path = downl_dir + software + "-" + version + "." + extension

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
                dynamic_ncols=True,
                # colour='blue',
                # text_colour='blue',
        ) as bar:
            for data in load.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)
    except Exception as e:
        print(e)
        os.remove(sv_path)

    tqdm.write(f'Downloaded {software} in version {version}: {sv_path}.')
    tqdm.write(f'staring verification of {software}')
    if os.path.exists(sv_path):
        result = verify(sv_path)
        if not result:
            tqdm.write(f'verification failed, deleting {software} from path {sv_path}')
            os.remove(sv_path)
        else:
            tqdm.write(f'verification successful.')


def download(platform, sw_list=[]):
    """downloads list of software"""
    path_init()
    if len(sw_list) == 0:
        sw_list = get_sw_list_for_platform(platform)

    for f in sw_list:
        download_sw(f, platform, DOWNLOAD_PATH)
    return DOWNLOAD_PATH + '/'


def download_gui(sw_list):
    """download methode for application gui"""
    def wrapper(app):
        app_name = app['program']
        app_platform = app['platform']
        app_version = app['version']

        download_sw(app_name, app_platform, app_version, DOWNLOAD_PATH)

    thread_map(wrapper, sw_list, position=1, leave=True)


if __name__ == '__main__':
    platform = 'win64'

    download(platform)
