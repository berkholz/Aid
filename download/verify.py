import hashlib

import gnupg
import requests
from tqdm import tqdm

from Db.database import get_checksum_link, get_sw_list_for_platform, get_software_link
from download.utils import *


def verify_downloads(platform, sw_list=[]):
    """methode initiates checksum and signature verification for given software list"""
    # when software list is empty, we take all available software for our platform
    if len(sw_list) == 0:
        sw_list = get_sw_list_for_platform(platform)

    # for every app we start the verification process
    for sw in sw_list:
        app_name = sw['program']
        app_platform = sw['platform']
        app_version = sw['version']

        # gets download link from db to get path and filename on system
        link = get_software_link(app_name, app_platform, app_version)

        extension = link.split('?')[0].split('.')[-1]

        if link.split('?')[0].split('.')[-2] == 'tar':
            extension = 'tar.' + extension

        if '/' in app_version:
            app_version = '_'.join(app_version.split('/'))

        dir = DOWNLOAD_PATH + "/" + sw + '/' + app_version + '/' + platform + '/'
        sv_path = dir + sw + "-" + app_version + "." + extension
        if os.path.exists(sv_path):
            # start verification of file
            if not verify(sv_path):
                return False
    return True


def verify(path):
    """initiates verification for a specific file"""
    file_name = path.split('/')[-1]
    platform = path.split('/')[-2].split('-')[0]
    software = file_name.split('-')[0]
    i = -1
    if file_name.split('.')[-2] == 'tar':
        i = -2
    software_version = ".".join(file_name.split('-')[1].split('.')[:i])

    # we get our verification source
    res = get_checksum_link(platform, software, software_version)
    if res is None:
        tqdm.write(f'software {software} version {software_version} not found in database')
        return False

    # we start verifying checksums
    hash_verify_status = verify_hash(path, software, res)

    # and the continue with signatures
    sig_verify_status = verify_signature(path, res)

    # check for failed verification
    if hash_verify_status == False or sig_verify_status == False:
        return False
    else:
        return True


def verify_hash(path, software, res):
    """checksum verifcation"""

    # we load the relevant source information in variables
    dwl_link = res[0]
    cs_type = res[1]
    cs_link = res[2]

    # first we check if there is a checksum available and how it is provided
    if cs_link:
        if cs_type == 'sha256_single':
            online_hash = get_single_line_file_hash(link=cs_link).lower()
        elif cs_type == 'sha256_multi':
            online_hash = get_multi_line_file_hash(cs_link, dwl_link).lower()
        elif cs_type == 'string' or cs_type == 'sha1_string':
            online_hash = cs_link.lower()
        else:
            return True

    # then we check if the local file matches that checksums
        with open(path, 'rb') as f:
            bytes = f.read()
            if cs_type in ['sha256_single', 'sha256_multi', 'string']:
                file_hash = hashlib.sha256(bytes).hexdigest()
            else:
                file_hash = hashlib.sha1(bytes).hexdigest()

        tqdm.write(f'Verifying hash of {software}({cs_type}):\n'
                   f'local\t:\t{file_hash}\n'
                   f'online\t:\t{online_hash}')

        return file_hash == online_hash

    else:
        return None


def download_file(url, local_filename):
    """Download a file from a URL and save it locally."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        # print(response.content)
        with open(local_filename, 'wb') as f:
            f.write(response.content)
        # print(f"Downloaded: {local_filename}")
    except requests.RequestException as e:
        tqdm.write(f"Error downloading {url}: {e}")
        return False
    return True


def import_key_from_url(key_url):
    """Import a public key from a URL."""
    gpg = gnupg.GPG()
    try:
        retry = 0
        response = requests.get(key_url, timeout=300)
        while response.status_code == 502 and retry < 5:
            response = requests.get(key_url, timeout=300)
            retry += 1

        # print(response.status_code)
        key_data = response.text
        import_result = gpg.import_keys(key_data)
        if import_result.count == 0:
            print("Error: No key was imported.")
            return False
        # print(f"Key imported successfully. Fingerprint: {import_result.fingerprints[0]}")
        return True
    except requests.RequestException as e:
        print(f"Error downloading or importing the key: {e}")
        return False


def verify_signature(file_path, res):
    """Verify a local file against its PGP signature downloaded from a URL."""
    signature_type = res[3]
    signature_url = res[4]
    hash_url = res[2]
    key_url = res[5]

    if signature_type in ['asc_file', 'sig_file', 'gpg_file']:
        checking_hash = False
        if not import_key_from_url(key_url):
            return False
        gpg = gnupg.GPG()

        # Check if the local file exists
        if not os.path.exists(file_path):
            tqdm.write(f"Error: The file {file_path} does not exist.")
            return False
        if hash_url is not None and hash_url + '.asc' == signature_url:

            hash_filename = 'tmp_hash'
            if not download_file(hash_url, hash_filename):
                return False
            file_path = hash_filename
            checking_hash = True

        # Download the signature file
        if signature_type == 'sig_file':
            signature_filename = "signature.sig"
        else:
            signature_filename = "signature.asc"

        if not download_file(signature_url, signature_filename):
            return False

        # Verify the signature
        with open(signature_filename, 'rb') as sig_file:
            verified = gpg.verify_file(sig_file, file_path)

        os.remove(signature_filename)
        if checking_hash:
            os.remove(hash_filename)

        if verified:
            tqdm.write("Signature verified successfully.")
            tqdm.write(f"Signed by: {verified.username}")
            return True
        else:
            tqdm.write("Signature verification failed.")
            tqdm.write(f"Status: {verified.problems}")
            return False


    elif signature_type is None:
        return True


def get_single_line_file_hash(link):
    # helper to get the checksum from a single lined sha256 file
    hash_file = requests.get(link)
    return hash_file.content.decode('utf-8').split('  ')[0]


def get_multi_line_file_hash(cs_link, file_link):
    # helper to get the checksum from a multi line sha256 file
    tmp = "/".join(file_link.split('/')[-3:])

    hash_file = requests.get(cs_link)
    lines = hash_file.content.decode('utf-8')

    rt_string = None
    for line in lines.split('\n'):
        if tmp in line:
            rt_string = line.split('  ')[0]
    if rt_string is None:
        tmp = "/".join(file_link.split('/')[-1:])
        for line in lines.split('\n'):
            if tmp in line:
                rt_string = line.split('  ')[0]
    return rt_string


if __name__ == '__main__':
    verify_downloads('win64')
