import datetime
import os
import re
from copyreg import dispatch_table
from urllib.request import urlretrieve

import requests

import Db.database as db

cwd_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOAD_PATH = os.path.join(cwd_dir, 'downloads/')
def path_init():
    """initializes the download-folder"""
    if not os.path.exists(DOWNLOAD_PATH):
        os.makedirs(DOWNLOAD_PATH)

def get_newest_link(software,platform):
    """database request for download-link of newest version"""
    links = db.get_software_links(software.lower(),platform.lower())
    newest = max(links.keys() ,key=lambda x: parse_version(x))
    return links[newest],newest


def parse_version(strg):
    """makes version comparable"""
    if '/' in strg:
        dt = datetime.datetime.strptime(strg, '%m/%d/%Y')
        return dt.timestamp()
    else:
        version = re.sub(r'[a-zA-Z]','',strg)
        return tuple (map(int, version.split('.')))

def download_sw(software,platform,path):
    """downloads single software"""
    link,version = get_newest_link(software,platform)
    extension = link.split('?')[0].split('.')[-1]

    print(f"Starting download of {software}, version {version}...")
    load = requests.get(link,timeout=300)

    if '/' in version:
        version = '_'.join(version.split('/'))
    sv_path = path+"/"+software+"-"+version+"."+extension
    if load.status_code == 200:
        with open(sv_path, 'wb') as file:
            file.write(load.content)
        print(f'Downloaded {software} in version {version}: {sv_path}.')
    else:
        print(f'Failed to download {software}.')


def download(sw_list,platform):
    """downloads list of software"""
    date_str = datetime.datetime.now().strftime('%d_%m_%Y')
    if not os.path.exists(DOWNLOAD_PATH+date_str):
        os.makedirs(DOWNLOAD_PATH+date_str)
    index=0
    index_str = ""
    while os.path.exists(DOWNLOAD_PATH+date_str+'/'+platform+index_str):
        index+=1
        index_str = "-"+str(index)
    path= DOWNLOAD_PATH+date_str+'/'+platform+index_str
    os.makedirs(path)

    for f in sw_list:
        download_sw(f,platform,path)



if __name__ == '__main__':
    softwares = [
        '7zip',
        'adobe_enterprise',
        'firefox_esr',
        'inkscape',
        'keepass',
        'notepad++',
        'putty',
        'sqlite_browser',
        'stunnel',
        'winscp',
        'gimp',
        'sqldeveloper',
        'sysinternal_utilities'
    ]

    download(softwares,'win64')