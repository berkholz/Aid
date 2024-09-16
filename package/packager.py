import hashlib
import os
import shutil
from datetime import datetime

import gnupg

from Db.database import get_verified_version,sqlite_db_file
from download.utils import DOWNLOAD_PATH


PACKAGE_PATH = 'C:/Users/***REMOVED***/Desktop/tmp_package/'
PACKAGE_NAME_PATTERN = 'AID_PACKAGE-{}-{}/'


download_path = DOWNLOAD_PATH

gpg = gnupg.GPG()

gpg.encoding = 'utf-8'


def package(sw_list,name):
    pkg_name = PACKAGE_NAME_PATTERN.format(datetime.now().strftime('%y_%m_%d'),name)
    pkg_path = PACKAGE_PATH+pkg_name
    os.makedirs(pkg_path,exist_ok=True)

    collect_software(sw_list,pkg_path)
    insert_db(pkg_path)
    generate_sums(pkg_path)
    return pkg_path

def collect_software(sw_list, dest_path):
    for sw in sw_list:

        app_name = sw['program']
        app_platform = sw['platform']
        app_version = sw['version']

        path = download_path+'/'+app_name+'/'+app_version+'/'+app_platform+'/'
        for filename in os.listdir(path):
            if filename.find(app_version) >=0:
                shutil.copy(os.path.join(path,filename),dest_path)

def insert_db(path):
    shutil.copy(sqlite_db_file,path)



def generate_sums(path):
    hash_file = path + 'sha256sum.txt'

    for filename in os.listdir(path):
        if 'sha256sum.txt' in filename:
            os.remove(os.path.join(path,filename))

    for filename in os.listdir(path):
        print(filename)

        if not 'sha256sum' in filename:
            temp_hash = hashlib.sha256()
            with open (os.path.join(path,filename),'rb') as f:
                fb = f.read(65536)
                while len(fb) > 0:
                    temp_hash.update(fb)
                    fb = f.read(65536)

            with open(hash_file,'a+') as f:
                f.write(f'{temp_hash.hexdigest()}  {filename}\n')
                f.close()

    with open(hash_file,'rb') as f:
        signed = gpg.sign_file(f,detach=True,output=f'{hash_file}.asc')

    print('generated sha256 sums and signature')






if __name__ == '__main__':
    package(['7zip','firefox_esr','putty'],'win64','Testpkg')

