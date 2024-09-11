import datetime
import os
import re
from sys import platform

import requests
from tqdm import tqdm

import Db.database as db
from Db.database import get_sw_list_for_platform, set_verified_version, get_verified_version
from download.utils import *
from download.verify import verify


def path_init():
    """initializes the download-folder"""
    if not os.path.exists(DOWNLOAD_PATH):
        os.makedirs(DOWNLOAD_PATH)


def download_sw(software,platform,path):
    """downloads single software"""
    link,version = get_newest_link(software,platform)

    extension = link.split('?')[0].split('.')[-1]

    if link.split('?')[0].split('.')[-2] == 'tar':
        extension = 'tar.'+extension

    dir = path+"/"+software+'/'+version+'/'+platform+'/'

    if not os.path.exists(dir):
        os.makedirs(dir,exist_ok=True)
    sv_path = dir +software+"-"+version+"."+extension

    verified_version = get_verified_version(software,platform)
    if os.path.exists(sv_path) and verified_version==version:
        return
    elif os.path.exists(sv_path):
        res = verify(sv_path)
        if res is True:
            print(f'verified unverified download: {software} version: {version}')
            return
        else:
            print('unverifyable Download found')

    print(f"Starting download of {software}, version {version}...")
    load = requests.get(link,timeout=300,stream=True)
    total = int(load.headers.get('content-length', 0))

    try:
        with open(sv_path, 'wb') as file,tqdm(
            desc=f'Downloading {software}',
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in load.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)
    except Exception as e:
        print(e)
        os.remove(sv_path)

    print(f'Downloaded {software} in version {version}: {sv_path}.')
    print(f'staring verification of {software}')
    result = verify(sv_path)
    if not result:
        print(f'verification failed, deleting {software} from path {sv_path}')
        os.remove(sv_path)
    else:
        print(f'verification successful.')



def download(platform,sw_list=[]):
    """downloads list of software"""
    path_init()
    if len(sw_list) == 0:
        sw_list = get_sw_list_for_platform(platform)

    for f in sw_list:
        download_sw(f,platform,DOWNLOAD_PATH)
    return DOWNLOAD_PATH + '/'



if __name__ == '__main__':
    platform = 'win64'

    download(platform)